# Generated by Django 5.0.3 on 2024-05-12 20:31

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0016_alter_cart_uuid_alter_order_cart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("e0653c95-e351-460d-9013-1635db00298c"),
                editable=False,
                verbose_name="Идентификатор пользователя",
            ),
        ),
    ]
