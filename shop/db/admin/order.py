from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from shop.db.admin import forms
from shop.db.models.order import Cart, OrderStatus


class OrderStatusFilter(admin.SimpleListFilter):
    title = _("Статус заказа")
    parameter_name = "order_status_filter"

    def lookups(self, request, model_admin):
        return ((os, os) for os in OrderStatus)

    def queryset(self, request, queryset):
        if self.value():
            kwargs = {"order__status": self.value()}
            return queryset.filter(**kwargs)
        return queryset.filter()


class CartAdmin(admin.ModelAdmin):
    search_fields = ["uuid", "created_at", "updated_at"]
    list_filter = [OrderStatusFilter]
    list_display = ["uuid", "product_units_html", "total", "status", "created_at", "updated_at"]
    list_display_links = None

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class ProductUnitCartAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class OrderAdmin(admin.ModelAdmin):
    search_fields = ["customer_id", "name", "phone", "email"]
    list_filter = ["status"]
    list_display = ["customer_id", "name", "phone", "email", "cart_html", "cart_total", "status"]

    form = forms.OrderForm
