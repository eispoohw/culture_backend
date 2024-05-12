from decimal import Decimal

from rest_framework import serializers

from shop.core.serializers.product_unit import ProductUnitSerializer
from shop.db.models import order


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = order.Cart
        fields = ["uuid", "created_at", "updated_at"]


class ProductUnitsCartSerializer(serializers.ModelSerializer):
    product_unit = ProductUnitSerializer()
    price_total = serializers.SerializerMethodField("get_price_total")

    @staticmethod
    def get_price_total(product_unit_cart):
        return Decimal(product_unit_cart.count * product_unit_cart.product_unit.price)

    class Meta:
        model = order.ProductUnitsCart
        fields = ["product_unit", "count", "price_total"]


class DetailedCartSerializer(serializers.ModelSerializer):
    product_units = ProductUnitsCartSerializer(many=True)

    class Meta:
        model = order.Cart
        fields = ["product_units", "uuid", "order"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = order.Order
        fields = ["name", "phone", "email", "cart"]
