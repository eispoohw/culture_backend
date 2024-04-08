from django.contrib import admin
from shop.db.models import product
from shop.db.models import product_unit
from shop.db.models import order

admin.site.register(product.Product)
admin.site.register(product.ProductMaterials)
admin.site.register(product.ProductImage)
admin.site.register(product.Color)
admin.site.register(product.Material)
admin.site.register(product.ProductCategory)

admin.site.register(product_unit.ProductUnit)
admin.site.register(product_unit.Size)

admin.site.register(order.Cart)
admin.site.register(order.Discounts)
admin.site.register(order.DiscountsCart)
admin.site.register(order.ProductUnitsCart)
admin.site.register(order.Order)
