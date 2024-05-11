from django.contrib import admin
from django.db.models import Count

from shop.db.admin import forms


class CartAdmin(admin.ModelAdmin):
    search_fields = ["uuid", "created_at", "updated_at"]
    list_display = ["uuid", "product_units_html", "created_at", "updated_at"]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
