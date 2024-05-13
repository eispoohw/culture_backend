import django_filters

from shop.db.models import product


class RootProductCategoryFilter(django_filters.Filter):
    def filter(self, qs, value: int):
        if value is not None:
            qs = qs.filter(parent_category__isnull=True)
        return qs


class ProductCategoryFilter(django_filters.FilterSet):
    parent = django_filters.NumberFilter(
        field_name="parent_category__slug",
        label="Родительская категория",
    )
    root = RootProductCategoryFilter()

    class Meta:
        model = product.ProductCategory
        fields = ["parent", "root"]


class ProductCategoryProductFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value is None:
            return qs
        try:
            selected_category = product.ProductCategory.objects.get(slug=value)
        except product.ProductCategory.DoesNotExist:
            return qs.none()

        children = selected_category.children.all()
        query = []
        if children is not None:
            query = list(children)
        query = query + [selected_category]
        qs = qs.filter(category__in=query)

        return qs


class ProductFilter(django_filters.FilterSet):
    materials = django_filters.CharFilter(field_name="materials__slug")
    colors = django_filters.CharFilter(field_name="colors__slug")
    category = ProductCategoryProductFilter()

    class Meta:
        model = product.Product
        fields = ["sex", "materials", "colors", "category"]
