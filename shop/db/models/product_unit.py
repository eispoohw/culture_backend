from django.core.validators import DecimalValidator, RegexValidator
from django.db import models
from django.utils.text import slugify

from shop.db.models.product import Product, ProductCategory


class Size(models.Model):
    """Размер единицы товара."""

    title = models.CharField(max_length=128, null=False, blank=False, unique=True, help_text="Название")
    slug = models.CharField(
        max_length=128,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
                message="Неверный формат",
                code="invalid_slug",
            )
        ],
        help_text="Идентификатор на английском языке",
    )
    product_category = models.ForeignKey(
        ProductCategory,
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

    title = models.CharField(max_length=128, null=False, blank=False, unique=True, help_text="Название")
    price = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        validators=[DecimalValidator],
        help_text="Цена товара",
    )
    size = models.ForeignKey(
        Size,
        related_name="product_units",
        on_delete=models.CASCADE,
        help_text="Размер единицы товара",
    )
    product = models.ForeignKey(Product, related_name="product_units", on_delete=models.CASCADE)
    reserved = models.BooleanField(default=False, null=False, help_text="Наличие брони")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, help_text="Дата обновления")

    def __str__(self):
        return self.title
