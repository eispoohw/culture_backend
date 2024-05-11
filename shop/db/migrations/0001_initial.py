# Generated by Django 5.0.3 on 2024-05-11 16:20

import colorfield.fields
import django.core.validators
import django.db.models.deletion
import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Color",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Уникальное название на русском языке",
                        max_length=128,
                        unique=True,
                        verbose_name="Название",
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        help_text="Уникальный идентификатор на английском языке",
                        max_length=128,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_slug",
                                message="Неверный формат",
                                regex="^[a-z0-9]+(?:-[a-z0-9]+)*$",
                            )
                        ],
                        verbose_name="Идентификатор на англ. языке",
                    ),
                ),
                (
                    "value",
                    colorfield.fields.ColorField(
                        default="#FFFFFFFF",
                        help_text="HEX-код цвета",
                        image_field=None,
                        max_length=25,
                        samples=None,
                        unique=True,
                        verbose_name="HEX-код цвета",
                    ),
                ),
            ],
            options={
                "verbose_name": "Цвет товара",
                "verbose_name_plural": "Цвета товаров",
            },
        ),
        migrations.CreateModel(
            name="Material",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Уникальное название на русском языке",
                        max_length=128,
                        unique=True,
                        verbose_name="Название",
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        help_text="Уникальный идентификатор на английском языке",
                        max_length=128,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_slug",
                                message="Неверный формат",
                                regex="^[a-z0-9]+(?:-[a-z0-9]+)*$",
                            )
                        ],
                        verbose_name="Идентификатор на англ. языке",
                    ),
                ),
            ],
            options={
                "verbose_name": "Материал товара",
                "verbose_name_plural": "Материалы товаров",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "title",
                    models.CharField(
                        help_text="Уникальное название на русском языке",
                        max_length=128,
                        verbose_name="Название",
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        editable=False,
                        help_text="Уникальный идентификатор на английском языке",
                        max_length=128,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_slug",
                                message="Неверный формат",
                                regex="^[a-z0-9]+(?:-[a-z0-9]+)*$",
                            )
                        ],
                        verbose_name="Идентификатор на англ. языке",
                    ),
                ),
                (
                    "article",
                    models.CharField(
                        help_text="Артикул (уникальный код товара)",
                        max_length=128,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Артикул",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Описание товара для отображения на сайте , может быть пустым",
                        null=True,
                        verbose_name="Описание товара",
                    ),
                ),
                (
                    "sex",
                    models.CharField(
                        choices=[("М", "мужчины"), ("Ж", "женщины"), ("У", "унисекс")],
                        default="У",
                        help_text="Для какого пола предназначен товар",
                        max_length=1,
                        verbose_name="Пол",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Дата создания"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
                ),
                (
                    "colors",
                    models.ManyToManyField(
                        help_text="Цвет(а) товара",
                        related_name="products",
                        to="shop.color",
                        verbose_name="Цвета",
                    ),
                ),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
            },
        ),
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Уникальное название на русском языке",
                        max_length=128,
                        unique=True,
                        verbose_name="Название",
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        help_text="Уникальный идентификатор на английском языке",
                        max_length=128,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_slug",
                                message="Неверный формат",
                                regex="^[a-z0-9]+(?:-[a-z0-9]+)*$",
                            )
                        ],
                        verbose_name="Идентификатор на англ. языке",
                    ),
                ),
                (
                    "category_level",
                    models.IntegerField(
                        default=1,
                        editable=False,
                        help_text='Уровень категории относительно других категорий, где 1 - корневая категория (например, "одежда")',
                        verbose_name="Уровень категории",
                    ),
                ),
                (
                    "parent_category",
                    models.ForeignKey(
                        blank=True,
                        help_text="Название родительской категории для текущей категории. Может быть пустым",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="shop.productcategory",
                        verbose_name="Родительская категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория товара",
                "verbose_name_plural": "Категории товаров",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                help_text="Категория товара",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="shop.productcategory",
                verbose_name="Категория",
            ),
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to="cultureshop/items", verbose_name="Изображение"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="shop.product",
                        verbose_name="Товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображение товара",
                "verbose_name_plural": "Изображения товаров",
            },
        ),
        migrations.CreateModel(
            name="ProductMaterials",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "percentage",
                    models.IntegerField(
                        help_text="Количество в процентах, может быть пустым",
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="Процент",
                    ),
                ),
                (
                    "material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_materials",
                        to="shop.material",
                        verbose_name="Материал",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_materials",
                        to="shop.product",
                        verbose_name="Товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "Процент материала в товаре",
                "verbose_name_plural": "Проценты материалов в товарах",
                "unique_together": {("product", "material")},
            },
        ),
        migrations.AddField(
            model_name="product",
            name="materials",
            field=models.ManyToManyField(
                help_text="Материал(ы) товара",
                related_name="products",
                through="shop.ProductMaterials",
                to="shop.material",
                verbose_name="Материалы",
            ),
        ),
    ]