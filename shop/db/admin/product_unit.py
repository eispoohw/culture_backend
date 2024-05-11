from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from shop.db.admin import forms
from shop.db.models.product import ProductCategory


class TopLevelCategoryFilter(admin.SimpleListFilter):
    title = _("Категория товаров")
    parameter_name = "top_level_categories"

    def lookups(self, request, model_admin):
        top_categories = ProductCategory.objects.filter(parent_category__isnull=True)
        return ((tp.id, tp.title) for tp in top_categories)

    def queryset(self, request, queryset):
        if self.value():
            kwargs = {"product_category": int(self.value())}
            return queryset.filter(**kwargs)
        return queryset.filter()


class SizeAdmin(admin.ModelAdmin):
    list_filter = [TopLevelCategoryFilter]
    search_fields = ["title", "slug", "product_category"]
    list_display = ["title", "slug", "product_category"]

    form = forms.SizeForm


class ProductUnitAdmin(admin.ModelAdmin):
    search_fields = ["title", "product__article", "product__title"]
    list_filter = ["size"]
    list_display = [
        "product",
        "images",
        "size",
        "price",
        "count",
        "available",
        "carts_without_order_count",
        "pending_orders_count",
        "confirmed_orders_count",
        "completed_orders_count",
        "cancelled_orders_count",
        "created_at",
        "updated_at",
    ]
