# Generated by Django 5.0.3 on 2024-05-11 20:59

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0008_remove_order_verified_alter_cart_uuid_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cart",
            options={
                "verbose_name": "КОРЗИНА ПОКУПАТЕЛЯ",
                "verbose_name_plural": "КОРЗИНЫ ПОКУПАТЕЛЕЙ",
            },
        ),
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.IntegerField(
                choices=[(0, "создан"), (1, "подтвержден"), (2, "выполнен")],
                default=0,
                help_text="Статус заказа",
                verbose_name="Статус",
            ),
        ),
        migrations.AlterField(
            model_name="cart",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("3fa89d32-ac7c-4155-869a-2a3fda201203"),
                editable=False,
                verbose_name="Идентификатор пользователя",
            ),
        ),
    ]
