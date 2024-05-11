import uuid

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.html import format_html
from shortuuid.django_fields import ShortUUIDField

from shop.db.models.product_unit import ProductUnit


class Cart(models.Model):
    """Корзина для заказа"""

    uuid = models.UUIDField(verbose_name="Идентификатор пользователя", null=False, editable=False, default=uuid.uuid4())
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, help_text="Дата обновления")

    def __str__(self):
        return str(self.uuid)

    def product_units(self):
        return ProductUnitsCart.objects.filter(cart=self)

    def product_units_html(self):
        rows = []
        for pu in self.product_units():
            rows.append(f"<li>{str(pu)}</li>")

        return format_html("".join(rows))


class ProductUnitsCart(models.Model):
    """Связь товаров и корзины"""

    product_unit = models.ForeignKey(ProductUnit, related_name="product_unit_cart", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name="product_unit_cart", on_delete=models.CASCADE)
    count = models.IntegerField(
        verbose_name="Количество",
        null=False,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Количество единиц товара в корзине",
    )

    def __str__(self):
        return f"{self.product_unit} - {self.count}"


class Order(models.Model):
    """Заказ"""

    customer_id = ShortUUIDField(length=8, max_length=8)
    name = models.CharField(max_length=128, null=False, help_text="Имя заказчика")
    phone = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex="^[+]7[0-9]{7,14}$",
                message="Неверный формат",
                code="invalid_phone",
            )
        ],
        null=False,
    )
    email = models.EmailField(null=False)
    cart = models.ForeignKey(Cart, related_name="order", on_delete=models.CASCADE)

    confirmed = models.BooleanField(default=False, null=False, help_text="Подтвержден ли заказ")
    completed = models.BooleanField(default=False, null=False, help_text="Выполнен ли заказ")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, help_text="Дата обновления")
