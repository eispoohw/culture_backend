from django.contrib import admin

from shop.db.admin import product as product_admin
from shop.db.models import order, product, product_unit

admin.site.register(product.Material, product_admin.MaterialAdmin)
admin.site.register(product.ProductCategory, product_admin.ProductCategoryAdmin)
admin.site.register(product.Color, product_admin.ColorAdmin)
admin.site.register(product.Product, product_admin.ProductAdmin)
admin.site.register(product.ProductMaterials, product_admin.ProductMaterialsAdmin)
admin.site.register(product.ProductImage, product_admin.ProductImageAdmin)

admin.site.register(product_unit.ProductUnit)
admin.site.register(product_unit.Size)

admin.site.register(order.Cart)
admin.site.register(order.Discounts)
admin.site.register(order.DiscountsCart)
admin.site.register(order.ProductUnitsCart)
admin.site.register(order.Order)
