from django.urls import path

from shop.core.views import order, product

urlpatterns = [
    path("materials", product.MaterialView.as_view()),
    path("categories", product.ProductCategoryView.as_view()),
    path("colors", product.ColorView.as_view()),
    path("products", product.ProductView.as_view()),
    path("products/<str:slug>", product.ProductPageView.as_view(lookup_field="slug")),
    path("cart", order.CartCreateAPIView.as_view({"post": "create", "delete": "destroy"})),
]
