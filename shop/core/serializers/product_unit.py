from rest_framework import serializers

from shop.db.models.product_unit import *


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"


class ProductUnitSerializer(serializers.ModelSerializer):
    size = SizeSerializer()

    class Meta:
        model = ProductUnit
        fields = ["id", "size", "count", "price", "product"]
