from rest_framework import serializers

from shop.core.serializers.product_unit import ProductUnitSerializer
from shop.db.models._base import Sex
from shop.db.models.product import *


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductCategoryWithHierarchySerializer(serializers.ModelSerializer):
    hierarchy = serializers.SerializerMethodField("get_hierarchy")
    hierarchy_list = serializers.SerializerMethodField("get_hierarchy_list")

    @staticmethod
    def get_hierarchy(product_category):
        return str(product_category)

    @staticmethod
    def get_hierarchy_list(product_category):
        return [ProductCategorySerializer(category).data for category in product_category.all_categories()]

    class Meta:
        model = ProductCategory
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    colored_box = serializers.SerializerMethodField("get_colored_box")

    @staticmethod
    def get_colored_box(color):
        return color.colored_box()

    class Meta:
        model = Color
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductMaterialsSerializer(serializers.ModelSerializer):
    material = MaterialSerializer()

    class Meta:
        model = ProductMaterials
        fields = ["material", "percentage"]


class ProductSerializer(serializers.ModelSerializer):
    product_materials = ProductMaterialsSerializer(many=True)
    colors = ColorSerializer(many=True)
    category = ProductCategoryWithHierarchySerializer()
    images = ProductImageSerializer(many=True)
    sex_label = serializers.SerializerMethodField("get_sex_label")
    product_units = serializers.SerializerMethodField('get_product_units')
    total_count = serializers.SerializerMethodField("get_total_count")

    @staticmethod
    def get_sex_label(product):
        return Sex(product.sex).label

    @staticmethod
    def get_total_count(product):
        return product.total_count()

    @staticmethod
    def get_product_units(product):
        available_pu = []

        for pu in product.product_units.all():
            if pu.count > 0:
                available_pu.append(pu)

        return ProductUnitSerializer(available_pu, many=True).data

    class Meta:
        model = Product
        fields = [
            "article",
            "product_materials",
            "colors",
            "category",
            "images",
            "sex",
            "sex_label",
            "title",
            "slug",
            "description",
            "product_units",
            "total_count",
        ]
