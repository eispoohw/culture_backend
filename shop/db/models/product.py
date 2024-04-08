from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.text import slugify


class Material(models.Model):
    """Материал из которого сделан товар."""

    title = models.CharField(
        max_length=128, null=False, blank=False, unique=True, help_text="Название"
    )
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

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProductCategory(models.Model):
    """Категория товара."""

    title = models.CharField(
        max_length=128, null=False, blank=False, unique=True, help_text="Название"
    )
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
    parent_category = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Color(models.Model):
    """Цвет товара."""
    title = models.CharField(
        max_length=128, null=False, blank=False, unique=True, help_text="Название"
    )
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
    value = ColorField(
        format="hexa", null=False, blank=False, unique=True, help_text="HEX-код цвета"
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Товар."""

    title = models.CharField(
        max_length=128, null=False, blank=False, help_text="Название"
    )
    article = models.CharField(
        max_length=128, primary_key=True, null=False, blank=False, help_text="Артикул"
    )
    description = models.TextField(null=True, blank=True, help_text="Описание товара")
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

    materials = models.ManyToManyField(
        Material,
        related_name="products",
        through="ProductMaterials",
        help_text="Материал(ы) товара",
    )
    colors = models.ManyToManyField(
        Color, related_name="products", help_text="Цвет(а) товара"
    )
    category = models.ForeignKey(
        ProductCategory,
        related_name="products",
        on_delete=models.CASCADE,
        help_text="Категория товара",
    )

    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, help_text="Дата обновления")

    def __str__(self):
        return f"[{self.article}] {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.article)
        super().save(*args, **kwargs)


class ProductMaterials(models.Model):
    """Процентный состав материала в товаре. Например, 70% хлопок, 30% полиэластан."""

    product = models.ForeignKey(
        Product, related_name="product_materials", on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        Material, related_name="product_materials", on_delete=models.CASCADE
    )
    percentage = models.IntegerField(
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Количество в процентах",
    )


class ProductImage(models.Model):
    """Изображение товара."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="cultureshop/items")
