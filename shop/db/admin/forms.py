from django import forms
from django.core.exceptions import ValidationError

from shop.db.models import product, product_unit


class ProductMaterialsForm(forms.ModelForm):
    class Meta:
        model = product.ProductMaterials
        fields = "__all__"

    def is_valid(self):
        current_sum_of_percents = sum([pm.percentage for pm in product.ProductMaterials.objects.filter(product=self.data.get("product"))])
        if current_sum_of_percents + int(self.data.get("percentage")) > 100:
            current_percents = product.Product.objects.get(article=self.data.get("product")).materials_percentage()
            self.add_error(
                "percentage",
                ValidationError(
                    "Сумма процентов материалов в товаре должна быть не больше 100." f"Текущее значение для выбранного товара: {current_percents}"
                ),
            )
            return False
        return super().is_valid()


class SizeForm(forms.ModelForm):
    class Meta:
        model = product_unit.Size
        fields = "__all__"

    product_category = forms.ModelChoiceField(
        queryset=product.ProductCategory.objects.filter(parent_category__isnull=True), required=False, label="Категория товара"
    )
