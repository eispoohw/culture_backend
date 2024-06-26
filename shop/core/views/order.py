import datetime
import os

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shop.core.serializers._base import CountSerializer, ErrorSerializer, UUIDSerializer
from shop.core.serializers.order import CartSerializer, DetailedCartSerializer, OrderSerializer
from shop.db.models.order import Cart, Order, ProductUnitsCart
from shop.db.models.product_unit import ProductUnit


class CartAPIView(ModelViewSet):
    serializer_class = CartSerializer
    post_response = openapi.Response("Успешно созданная корзина", CartSerializer)
    delete_response = openapi.Response("Количество удаленных корзин", CountSerializer)
    detailed_response = openapi.Response("Детализированная корзина", DetailedCartSerializer)
    error_response = openapi.Response("Ошибка запроса", ErrorSerializer)
    filter_backends = []

    def get_queryset(self):
        return Cart.objects.all()

    @staticmethod
    def validate_request(func):
        def inner(*args, **kwargs):
            try:
                req_headers = args[1].META
                x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for_value:
                    ip_addr = x_forwarded_for_value.split(',')[-1].strip()
                else:
                    ip_addr = req_headers.get('REMOTE_ADDR')
                permitted_ips = os.getenv('ORDER_REQUESTS_PERMITTED_IPS').split(', ')
                assert ip_addr in permitted_ips
            except AssertionError:
                return Response(403)
            return func(*args, **kwargs)

        return inner

    @swagger_auto_schema(request_body=UUIDSerializer, responce_body=CartSerializer, responses={200: post_response})
    @validate_request
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    @swagger_auto_schema(responce_body=CountSerializer, responses={200: delete_response})
    @validate_request
    def destroy(self, *args, **kwargs):
        no_order_carts = Cart.objects.filter(order__isnull=True)
        old_carts = no_order_carts.filter(created_at__lt=datetime.datetime.utcnow() - datetime.timedelta(days=3))

        response_data = CountSerializer({"count": len(old_carts)}).data
        old_carts.delete()

        return Response(status=200, data=response_data)

    @swagger_auto_schema(responce_body=DetailedCartSerializer, responses={200: detailed_response, 400: error_response})
    @validate_request
    def add(self, *args, **kwargs):
        try:
            cart = Cart.objects.get(uuid__exact=kwargs.get("uuid"))
        except Exception as exc:
            return Response(status=400, data={"error": str(exc)})

        try:
            product_unit = ProductUnit.objects.get(id=kwargs.get("id"))
            assert product_unit.count > 0, "Товар закончился"
        except Exception as exc:
            return Response(status=400, data={"error": str(exc)})

        try:
            product_unit_cart = ProductUnitsCart.objects.get(cart=cart, product_unit=product_unit)
            product_unit_cart.count += 1
        except ProductUnitsCart.DoesNotExist:
            product_unit_cart = ProductUnitsCart(cart=cart, product_unit=product_unit, count=1)

        product_unit_cart.save()
        cart = Cart.objects.get(id=cart.id)
        return Response(status=200, data=DetailedCartSerializer(cart).data)

    @swagger_auto_schema(responce_body=DetailedCartSerializer, responses={200: detailed_response, 400: error_response})
    @validate_request
    def remove(self, *args, **kwargs):
        try:
            cart = Cart.objects.get(uuid__exact=kwargs.get("uuid"))
        except Exception as exc:
            return Response(status=400, data={"error": str(exc)})

        try:
            product_unit = ProductUnit.objects.get(id=kwargs.get("id"))
        except Exception as exc:
            return Response(status=400, data={"error": str(exc)})

        try:
            product_unit_cart = ProductUnitsCart.objects.get(cart=cart, product_unit=product_unit)
        except ProductUnitsCart.DoesNotExist:
            return Response(status=400, data={"error": "В корзине нет такого товара"})
        except Exception as exc:
            return Response(status=400, data={"error": str(exc)})

        product_unit_cart.count -= 1
        if product_unit_cart.count <= 0:
            product_unit_cart.delete()
        else:
            product_unit_cart.save()

        cart = Cart.objects.get(id=cart.id)
        return Response(status=200, data=DetailedCartSerializer(cart).data)


class DetailedCartView(generics.RetrieveAPIView):
    lookup_field = "uuid"
    queryset = Cart.objects.all()
    serializer_class = DetailedCartSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(uuid=request.data.get("cart"))
        except Exception as exc:
            return Response(status=400, data={"error": str(exc)})

        request.data["cart"] = cart.id
        print(request)
        return super().create(request, *args, **kwargs)
