from django.contrib import admin
from django.db.models import Count

from shop.core.admin import forms


class MaterialAdmin(admin.ModelAdmin):
    search_fields = ["title", "slug"]
    list_display = ["title", "slug", "products_count"]

    def get_queryset(self, request):
        qs = super(MaterialAdmin, self).get_queryset(request)
        qs = qs.annotate(Count("products"))
        return qs

    def products_count(self, obj) -> int:
        return obj.products__count

    products_count.short_description = "Количество товаров"
    products_count.admin_order_field = "products__count"


class ProductCategoryAdmin(admin.ModelAdmin):
    list_filter = ["category_level"]
    search_fields = ["title", "slug", "category_level"]
    list_display = ["title", "slug", "category_level", "hierarchy", "products_count"]

    def get_queryset(self, request):
        qs = super(ProductCategoryAdmin, self).get_queryset(request)
        qs = qs.annotate(Count("products"))
        return qs

    def hierarchy(self, obj) -> str:
        return str(obj)

    hierarchy.short_description = "Иерархия"

    def products_count(self, obj) -> int:
        return obj.products__count

    products_count.short_description = "Количество товаров"
    products_count.admin_order_field = "products__count"


class ColorAdmin(admin.ModelAdmin):
    search_fields = ["title", "slug"]
    list_display = ["title", "colored_box", "slug", "value", "products_count"]

    def get_queryset(self, request):
        qs = super(ColorAdmin, self).get_queryset(request)
        qs = qs.annotate(Count("products"))
        return qs

    def products_count(self, obj) -> int:
        return obj.products__count

    products_count.short_description = "Количество товаров"
    products_count.admin_order_field = "products__count"


class ProductAdmin(admin.ModelAdmin):
    search_fields = ["title", "article"]
    list_filter = ["sex", "colors", "materials", "category"]
    list_display = ["title", "images_field", "article", "sex", "category", "colors_field", "materials_percentage", "created_at", "updated_at"]


class ProductMaterialsAdmin(admin.ModelAdmin):
    search_fields = ["product", "material", "percentage"]
    list_filter = ["product", "material", "percentage"]
    list_display = ["product", "material", "percentage"]

    form = forms.ProductMaterialsForm


class ProductImageAdmin(admin.ModelAdmin):
    search_fields = ["product__title", "product__article"]
    list_display = ["product", "image_html_field"]
