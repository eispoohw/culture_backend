from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify

from shop.db.models._base import get_slug_kwargs, get_title_kwargs
from shop.db.models.product import Product, ProductCategory


class Size(models.Model):
    """Размер единицы товара."""

    class Meta:
        verbose_name = "Размер единицы товара"
        verbose_name_plural = "Размеры единицы товара"

    title = models.CharField(**get_title_kwargs())
    slug = models.CharField(**get_slug_kwargs())
    product_category = models.ForeignKey(
        ProductCategory,
        verbose_name="Категория товаров",
        null=True,
        related_name="product_category_sizes",
        on_delete=models.CASCADE,
        help_text="Категория товаров для которой создан размер",
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProductUnit(models.Model):
    """Единица товара."""

    class Meta:
        verbose_name = "ЕДИНИЦА ТОВАРА"
        verbose_name_plural = "ЕДИНИЦЫ ТОВАРОВ"
        unique_together = ("product", "size", "price")

    product = models.ForeignKey(Product, verbose_name="Продукт", related_name="product_units", on_delete=models.CASCADE)
    size = models.ForeignKey(
        Size,
        verbose_name="Размеер",
        related_name="product_units",
        on_delete=models.CASCADE,
        help_text="Размер единицы товара",
    )
    price = models.DecimalField(
        verbose_name="Цена",
        max_length=128,
        null=False,
        blank=False,
        decimal_places=2,
        max_digits=10,
        help_text="Цена товара в рублях",
    )
    count = models.IntegerField(
        verbose_name="Количество в наличии",
        null=False,
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Количество единиц товара в наличии",
    )
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True, help_text="Дата создания")
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True, help_text="Дата обновления")

    def __str__(self):
        return f"{self.product} - {self.size}"

    def carts(self):
        return self.product_unit_cart.all()

    def carts_without_order(self):
        return self.carts().filter(cart__order__isnull=True)

    def carts_without_order_count(self):
        return sum([obj.count for obj in self.carts_without_order()])

    def pending_orders(self):
        return self.carts().filter(cart__order__confirmed=False)

    def pending_orders_count(self):
        return sum([obj.count for obj in self.pending_orders()])

    def confirmed_orders(self):
        return self.carts().filter(cart__order__confirmed=True).filter(cart__order__completed=False)

    def confirmed_orders_count(self):
        return sum([obj.count for obj in self.confirmed_orders()])

    def completed_orders(self):
        return self.product_unit_cart.filter(cart__order__completed=True)

    def completed_orders_count(self):
        return sum([obj.count for obj in self.completed_orders()])

    def available(self):
        return self.count - self.confirmed_orders_count()

    def images(self):
        return self.product.images_field()

    carts_without_order_count.short_description = "Еще без заказа"
    pending_orders_count.short_description = "Ожидают подтверждения"
    confirmed_orders_count.short_description = "Ожидают самовывоз"
    completed_orders_count.short_description = "Продано"
    available.short_description = "Не зарезервировано"
    images.short_description = "Изображения"
