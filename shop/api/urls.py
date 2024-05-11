from django.urls import path

from shop.core.views import order

urlpatterns = [
    path("cart", order.CartCreateAPIView.as_view({"post": "create", "delete": "destroy"})),
]
