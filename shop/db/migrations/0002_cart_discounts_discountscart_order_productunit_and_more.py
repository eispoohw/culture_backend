# Generated by Django 5.0.3 on 2024-05-11 16:22

import django.core.validators
import django.db.models.deletion
import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
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
                ("uuid", models.UUIDField()),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="Дата создания"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="Дата обновления"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Discounts",
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
                ("title", models.CharField(help_text="Название акции", max_length=256)),
                ("time_from", models.DateTimeField(help_text="Дата начала акции")),
                ("time_to", models.DateTimeField(help_text="Дата окончания акции")),
                (
                    "description",
                    models.TextField(help_text="Описание акции", null=True),
                ),
                (
                    "should_describe",
                    models.BooleanField(
                        default=False,
                        help_text="Необходимо ли показывать описание акции",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discounts",
                        to="shop.product",
                    ),
                ),
                (
                    "product_category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discounts",
                        to="shop.productcategory",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DiscountsCart",
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
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discounts_cart",
                        to="shop.cart",
                    ),
                ),
                (
                    "discount",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discounts_cart",
                        to="shop.discounts",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
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
                    "customer_id",
                    shortuuid.django_fields.ShortUUIDField(alphabet=None, length=8, max_length=8, prefix=""),
                ),
                ("name", models.CharField(help_text="Имя заказчика", max_length=128)),
                (
                    "phone",
                    models.CharField(
                        max_length=16,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_phone",
                                message="Неверный формат",
                                regex="^[+]7[0-9]{7,14}$",
                            )
                        ],
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                (
                    "verified",
                    models.BooleanField(default=False, help_text="Проверен ли заказ"),
                ),
                (
                    "confirmed",
                    models.BooleanField(default=False, help_text="Подтвержден ли заказ"),
                ),
                (
                    "completed",
                    models.BooleanField(default=False, help_text="Выполнен ли заказ"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="Дата создания"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="Дата обновления"),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order",
                        to="shop.cart",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductUnit",
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
                    models.CharField(help_text="Название", max_length=128, unique=True),
                ),
                (
                    "price",
                    models.CharField(
                        help_text="Цена товара",
                        max_length=128,
                        validators=[django.core.validators.DecimalValidator],
                    ),
                ),
                (
                    "count",
                    models.IntegerField(
                        default=0,
                        help_text="Количество единиц товара в наличии",
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Количество в наличии",
                    ),
                ),
                (
                    "reserved",
                    models.BooleanField(default=False, help_text="Наличие брони"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="Дата создания"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="Дата обновления"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_units",
                        to="shop.product",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="discounts",
            name="product_unit",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="discounts",
                to="shop.productunit",
            ),
        ),
        migrations.CreateModel(
            name="ProductUnitsCart",
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
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_unit_cart",
                        to="shop.cart",
                    ),
                ),
                (
                    "product_unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_unit_cart",
                        to="shop.productunit",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Size",
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
                    "product_category",
                    models.ForeignKey(
                        help_text="Категория товаров для которой создан размер",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_category_sizes",
                        to="shop.productcategory",
                        verbose_name="Категория товаров",
                    ),
                ),
            ],
            options={
                "verbose_name": "Размер единицы товара",
                "verbose_name_plural": "Размеры единицы товара",
            },
        ),
        migrations.AddField(
            model_name="productunit",
            name="size",
            field=models.ForeignKey(
                help_text="Размер единицы товара",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_units",
                to="shop.size",
            ),
        ),
    ]
