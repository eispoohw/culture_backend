from django import forms
from django.core.exceptions import ValidationError

from shop.db.models import order, product, product_unit
from shop.db.models._base import OrderStatus


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


class OrderForm(forms.ModelForm):
    class Meta:
        model = order.Order
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        order = kwargs.get("instance")
        if order is None:
            return

        match order.status:
            case OrderStatus.CREATED:
                field_kwargs = {
                    "choices": (
                        (OrderStatus.CREATED, OrderStatus.CREATED),
                        (OrderStatus.CONFIRMED, OrderStatus.CONFIRMED),
                        (OrderStatus.CANCELLED, OrderStatus.CANCELLED),
                    ),
                    "disabled": False,
                }
            case OrderStatus.CONFIRMED:
                field_kwargs = {
                    "choices": (
                        (OrderStatus.CONFIRMED, OrderStatus.CONFIRMED),
                        (OrderStatus.CANCELLED, OrderStatus.CANCELLED),
                        (OrderStatus.COMPLETED, OrderStatus.COMPLETED),
                    ),
                    "disabled": False,
                }
            case OrderStatus.COMPLETED:
                field_kwargs = {"choices": ((OrderStatus.COMPLETED, OrderStatus.COMPLETED),), "disabled": True}
            case OrderStatus.CANCELLED:
                field_kwargs = {"choices": ((OrderStatus.CANCELLED, OrderStatus.CANCELLED),), "disabled": True}
            case _:
                field_kwargs = {"choices": OrderStatus, "disabled": False}

        self.fields["status"] = forms.ChoiceField(**field_kwargs)
        self.fields["status"].value = kwargs.get("instance").status
