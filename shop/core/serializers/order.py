from rest_framework import serializers

from shop.db.models import order


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = order.Cart
        fields = ["uuid", "created_at", "updated_at"]
