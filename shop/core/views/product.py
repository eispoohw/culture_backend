from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

import shop.core.filters as filters
from shop.core.serializers.product import ColorSerializer, MaterialSerializer, ProductCategoryWithHierarchySerializer, \
    ProductSerializer
from shop.db.models.product import Color, Material, Product, ProductCategory


class MaterialView(generics.ListAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filter_backends = []


class ProductCategoryView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryWithHierarchySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ProductCategoryFilter


class ColorView(generics.ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    filter_backends = []


class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = filters.ProductFilter
    search_fields = ["title", "slug", "article", "description", "colors__title"]
    ordering_fields = ["created_at", "product_units__price"]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        filtered_data = []

        for row in response.data:
            for pu in row['product_units']:
                if pu['count'] > 0:
                    filtered_data.append(row)
                    break

        response.data = filtered_data
        return response


class ProductPageView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = []
