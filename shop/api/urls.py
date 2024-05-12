from django.urls import path

from shop.core.views import order, product

urlpatterns = [
    path("materials", product.MaterialView.as_view()),
    path("categories", product.ProductCategoryView.as_view()),
    path("colors", product.ColorView.as_view()),
    path("products", product.ProductView.as_view()),
    path("products/<str:slug>", product.ProductPageView.as_view(lookup_field="slug")),
    path("cart", order.CartAPIView.as_view({"post": "create", "delete": "destroy"})),
    path("cart/<str:uuid>/add/<int:id>", order.CartAPIView.as_view({"get": "add"})),
    path("cart/<str:uuid>/remove/<int:id>", order.CartAPIView.as_view({"get": "remove"})),
    path("cart/<str:uuid>", order.DetailedCartView.as_view()),
    path("order", order.OrderCreateView.as_view()),
]
