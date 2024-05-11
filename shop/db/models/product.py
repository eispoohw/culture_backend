from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from shop.db.models._base import get_slug_kwargs, get_title_kwargs


class Material(models.Model):
    """Материал из которого сделан товар."""

    class Meta:
        verbose_name = "Материал товара"
        verbose_name_plural = "Материалы товаров"

    title = models.CharField(**get_title_kwargs())
    slug = models.CharField(**get_slug_kwargs())

    def save(self, *args, **kwargs) -> None:
        self.title = self.title.lower()
        self.slug = self.slug.lower()

        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class ProductCategory(models.Model):
    """Категория товара."""

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

    title = models.CharField(**get_title_kwargs())
    slug = models.CharField(**get_slug_kwargs())
    category_level = models.IntegerField(
        verbose_name="Уровень категории",
        null=False,
        default=1,
        editable=False,
        help_text='Уровень категории относительно других категорий, где 1 - корневая категория (например, "одежда")',
    )
    parent_category = models.ForeignKey(
        "self",
        verbose_name="Родительская категория",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
        help_text="Название родительской категории для текущей категории. Может быть пустым",
    )

    def __str__(self):
        categories = [self.title]
        parent = self.parent_category

        while parent:
            categories.append(parent.title)
            parent = parent.parent_category

        return " - ".join(categories[::-1])

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        self.slug = self.slug.lower()

        if self.parent_category is not None:
            self.category_level = self.parent_category.category_level + 1

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


class Color(models.Model):
    """Цвет товара."""

    class Meta:
        verbose_name = "Цвет товара"
        verbose_name_plural = "Цвета товаров"

    title = models.CharField(**get_title_kwargs())
    slug = models.CharField(**get_slug_kwargs())
    value = ColorField(verbose_name="HEX-код цвета", format="hexa", null=False, blank=False, unique=True, help_text="HEX-код цвета")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.lower()

        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def colored_box(self):
        return format_html(
            '<div style="background-color: {}; border:1px solid black; width: 30px; height: 30px;"></div>',
            self.value,
        )

    colored_box.short_description = ""


class Product(models.Model):
    """Товар."""

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    class Sex(models.TextChoices):
        MEN = "М", _("мужчины")
        WOMAN = "Ж", _("женщины")
        UNISEX = "У", _("унисекс")

    title = models.CharField(**get_title_kwargs(is_unique=False))
    slug = models.CharField(**get_slug_kwargs(editable=False))

    article = models.CharField(
        verbose_name="Артикул", max_length=128, primary_key=True, null=False, blank=False, help_text="Артикул (уникальный код товара)"
    )
    description = models.TextField(
        verbose_name="Описание товара", null=True, blank=True, help_text="Описание товара для отображения на сайте , может быть пустым"
    )
    sex = models.CharField(verbose_name="Пол", max_length=1, choices=Sex, default=Sex.UNISEX, help_text="Для какого пола предназначен товар")

    materials = models.ManyToManyField(
        Material,
        verbose_name="Материалы",
        related_name="products",
        through="ProductMaterials",
        help_text="Материал(ы) товара",
    )
    colors = models.ManyToManyField(Color, verbose_name="Цвета", related_name="products", help_text="Цвет(а) товара")
    category = models.ForeignKey(
        ProductCategory,
        verbose_name="Категория",
        related_name="products",
        on_delete=models.CASCADE,
        help_text="Категория товара",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"[{self.article}] {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.article)
        super().save(*args, **kwargs)

    def materials_percentage(self):
        return ", ".join([str(pm) for pm in self.product_materials.all()])

    def colors_field(self):
        return format_html("".join([color.colored_box() for color in self.colors.all()]))

    def images_field(self):
        html_images = []
        for obj in self.images.all():
            html_images.append(obj.image_html_field())
        return format_html("".join(html_images))

    colors_field.short_description = "Цвета"
    materials_percentage.short_description = "Материалы"
    images_field.short_description = "Изображения"


class ProductMaterials(models.Model):
    """Процентный состав материала в товаре. Например, 70% хлопок, 30% полиэластан."""

    class Meta:
        verbose_name = "Процент материала в товаре"
        verbose_name_plural = "Проценты материалов в товарах"
        unique_together = ("product", "material")

    product = models.ForeignKey(Product, verbose_name="Товар", related_name="product_materials", on_delete=models.CASCADE)
    material = models.ForeignKey(Material, verbose_name="Материал", related_name="product_materials", on_delete=models.CASCADE)
    percentage = models.IntegerField(
        verbose_name="Процент",
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Количество в процентах, может быть пустым",
    )

    def _get_percentage_str(self) -> str:
        if self.percentage is None:
            return ""

        return " " + str(self.percentage) + "%"

    def __str__(self):
        return str(self.material) + self._get_percentage_str()

    def save(self, *args, **kwargs):
        current_sum_of_percents = sum([pm.percentage for pm in ProductMaterials.objects.filter(product=self.product)])
        if current_sum_of_percents + self.percentage > 100:
            raise ValidationError("Сумма процентов материалов в товаре должна быть не больше 100")
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """Изображение товара."""

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"

    product = models.ForeignKey(Product, verbose_name="Товар", related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Изображение", upload_to="cultureshop/items")

    def image_html_field(self):
        return format_html(f'<img style="max-height: 100px; margin: 2px;" src="{self.image.url}"></img>')

    image_html_field.short_description = "Изображение"

    def __str__(self):
        return str(self.product)
