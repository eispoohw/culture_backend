import uuid

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.html import format_html
from shortuuid.django_fields import ShortUUIDField

from shop.db.models._base import OrderStatus, get_created_at_kwargs, get_updated_at_kwargs
from shop.db.models.product_unit import ProductUnit


class Cart(models.Model):
    """Корзина для заказа"""

    class Meta:
        verbose_name = "Корзина покупателя"
        verbose_name_plural = "Корзины покупателей"

    uuid = models.UUIDField(verbose_name="Идентификатор пользователя", null=False, editable=False, default=uuid.uuid4())
    created_at = models.DateTimeField(**get_created_at_kwargs())
    updated_at = models.DateTimeField(**get_updated_at_kwargs())

    def __str__(self):
        return str(self.uuid)

    def product_units(self):
        return ProductUnitsCart.objects.filter(cart=self)

    def product_units_html(self):
        rows = []
        for i, pu in enumerate(self.product_units()):
            rows.append(
                f"<b>{i + 1}. {str(pu.product_unit.product.title)}</b><br>"
                f"Размер: {str(pu.product_unit.size)}<br>"
                f"Количество: {str(pu.count)}<br>"
                f"Стоимость: {str(pu.product_unit.price)}<br>"
                f"<br>"
            )

        return format_html("".join(rows))

    def total(self):
        total = 0
        for pu in self.product_units():
            total += pu.product_unit.price * pu.count
        return total

    def status(self):
        return self.order.get(cart_id=self.id).status

    product_units_html.short_description = "Корзина"
    total.short_description = "Итоговая стоимость"
    status.short_description = "Статус"
    status.admin_order_field = "order__status"


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

    class Meta:
        verbose_name = "ЗАКАЗ ПОКУПАТЕЛЯ"
        verbose_name_plural = "ЗАКАЗЫ ПОКУПАТЕЛЕЙ"

    customer_id = ShortUUIDField(verbose_name="Идентификатор заказа", length=8, max_length=8)
    name = models.CharField(max_length=128, null=False, verbose_name="Имя заказчика")
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
        verbose_name="Номер телефона заказчика",
    )
    email = models.EmailField(verbose_name="Электронная почта заказчика", null=False)
    cart = models.ForeignKey(Cart, verbose_name="Корзина", related_name="order", on_delete=models.CASCADE)

    status = models.CharField(verbose_name="Статус", choices=OrderStatus, default=OrderStatus.CREATED, help_text="Статус заказа")

    created_at = models.DateTimeField(**get_created_at_kwargs())
    updated_at = models.DateTimeField(**get_updated_at_kwargs())

    def cart_html(self):
        return self.cart.product_units_html()

    def cart_total(self):
        return self.cart.total()

    def __str__(self):
        return str(self.customer_id)

    cart_html.short_description = "Корзина"
    cart_total.short_description = "К оплате"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        raise NotImplemented
