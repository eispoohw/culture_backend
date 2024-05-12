from rest_framework import serializers

from shop.db.models.product import *


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductCategoryWithHierarchySerializer(serializers.ModelSerializer):
    hierarchy = serializers.SerializerMethodField('get_hierarchy')
    hierarchy_list = serializers.SerializerMethodField('get_hierarchy_list')

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
    colored_box = serializers.SerializerMethodField('get_colored_box')

    @staticmethod
    def get_colored_box(color):
        return color.colored_box()

    class Meta:
        model = Color
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductMaterialsSerializer(serializers.ModelSerializer):
    material = MaterialSerializer()

    class Meta:
        model = ProductMaterials
        fields = ['material', 'percentage']


class ProductSerializer(serializers.ModelSerializer):
    product_materials = ProductMaterialsSerializer(many=True)
    colors = ColorSerializer(many=True)
    category = ProductCategoryWithHierarchySerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"
