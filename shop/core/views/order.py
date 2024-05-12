import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shop.core.serializers._base import CountSerializer, UUIDSerializer
from shop.core.serializers.order import CartSerializer
from shop.db.models.order import Cart


class CartCreateAPIView(ModelViewSet):
    serializer_class = CartSerializer
    post_response = openapi.Response("Успешно созданная корзина", CartSerializer)
    delete_response = openapi.Response("Количество удаленных корзин", CountSerializer)

    def get_queryset(self):
        return Cart.objects.all()

    @swagger_auto_schema(request_body=UUIDSerializer, responce_body=CartSerializer, responses={200: post_response})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(responce_body=CountSerializer, responses={200: delete_response})
    def destroy(self, request, *args, **kwargs):
        no_order_carts = Cart.objects.filter(order__isnull=True)
        old_carts = no_order_carts.filter(created_at__lt=datetime.datetime.utcnow() - datetime.timedelta(days=3))

        response_data = CountSerializer({"count": len(old_carts)}).data
        old_carts.delete()

        return Response(status=200, data=response_data)
