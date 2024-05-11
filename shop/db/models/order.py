from django.core.validators import RegexValidator
from django.db import models
from shortuuid.django_fields import ShortUUIDField

from shop.db.models.product import Product, ProductCategory
from shop.db.models.product_unit import ProductUnit


class Discounts(models.Model):
    """Скидки"""

    title = models.CharField(max_length=256, null=False, blank=False, help_text="Название акции")
    time_from = models.DateTimeField(null=False, help_text="Дата начала акции")
    time_to = models.DateTimeField(null=False, help_text="Дата окончания акции")

    description = models.TextField(null=True, help_text="Описание акции")

    should_describe = models.BooleanField(null=False, default=False, help_text="Необходимо ли показывать описание акции")

    product_unit = models.ForeignKey(ProductUnit, null=True, related_name="discounts", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, related_name="discounts", on_delete=models.CASCADE)
    product_category = models.ForeignKey(ProductCategory, null=True, related_name="discounts", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.product_unit is None and self.product is None and self.product_category is None:
            raise ValueError("Необходимо выбрать товар, категорию товаров или единицу товара")
        super().save(*args, **kwargs)


class Cart(models.Model):
    """Корзина для заказа"""

    uuid = models.UUIDField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, help_text="Дата обновления")


class ProductUnitsCart(models.Model):
    """Связь товаров и корзины"""

    product_unit = models.ForeignKey(ProductUnit, related_name="product_unit_cart", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name="product_unit_cart", on_delete=models.CASCADE)


class DiscountsCart(models.Model):
    """Связь скидок и корзины"""

    discount = models.ForeignKey(Discounts, related_name="discounts_cart", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name="discounts_cart", on_delete=models.CASCADE)


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

    verified = models.BooleanField(default=False, null=False, help_text="Проверен ли заказ")
    confirmed = models.BooleanField(default=False, null=False, help_text="Подтвержден ли заказ")
    completed = models.BooleanField(default=False, null=False, help_text="Выполнен ли заказ")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, help_text="Дата обновления")
