# Generated by Django 5.0.3 on 2024-05-11 21:46

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0012_alter_cart_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Дата создания"),
        ),
        migrations.AlterField(
            model_name="cart",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
        ),
        migrations.AlterField(
            model_name="cart",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("21740306-a340-4602-a6dc-36f29453b3ae"),
                editable=False,
                verbose_name="Идентификатор пользователя",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Дата создания"),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.IntegerField(
                choices=[
                    ("создан", "создан"),
                    ("подтвержден", "подтвержден"),
                    ("выполнен", "выполнен"),
                    ("отменен", "отменен"),
                    ("возвращен", "возвращен"),
                ],
                default="создан",
                help_text="Статус заказа",
                verbose_name="Статус",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
        ),
        migrations.AlterField(
            model_name="productunit",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Дата создания"),
        ),
        migrations.AlterField(
            model_name="productunit",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
        ),
    ]