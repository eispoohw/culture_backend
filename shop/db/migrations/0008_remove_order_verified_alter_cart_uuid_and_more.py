# Generated by Django 5.0.3 on 2024-05-11 20:49

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0007_remove_discountscart_discount_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="verified",
        ),
        migrations.AlterField(
            model_name="cart",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("dffa21bf-1011-481b-b87d-cd12ac1743a9"),
                editable=False,
                verbose_name="Идентификатор пользователя",
            ),
        ),
        migrations.AlterField(
            model_name="productunit",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                help_text="Дата создания",
                verbose_name="Дата создания",
            ),
        ),
        migrations.AlterField(
            model_name="productunit",
            name="size",
            field=models.ForeignKey(
                help_text="Размер единицы товара",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_units",
                to="shop.size",
                verbose_name="Размеер",
            ),
        ),
        migrations.AlterField(
            model_name="productunit",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                help_text="Дата обновления",
                verbose_name="Дата обновления",
            ),
        ),
    ]
