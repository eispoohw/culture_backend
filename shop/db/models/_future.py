from django.db import models

from shop.db.models.order import Cart
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


class DiscountsCart(models.Model):
    """Связь скидок и корзины"""

    discount = models.ForeignKey(Discounts, related_name="discounts_cart", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name="discounts_cart", on_delete=models.CASCADE)
