# Generated by Django 5.0.3 on 2024-05-11 17:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_alter_productunit_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="productunit",
            name="title",
            field=models.CharField(
                default="aa",
                help_text="Уникальное название на русском языке",
                max_length=128,
                verbose_name="Название",
            ),
        ),
        migrations.AlterField(
            model_name="productunit",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_units",
                to="shop.product",
                verbose_name="Продукт",
            ),
        ),
    ]
