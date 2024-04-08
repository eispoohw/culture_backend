from django.contrib.postgres.fields import ArrayField
from django.core.validators import DecimalValidator
from django.db import models


class ItemQuantity(models.Model):
    available = models.CharField(
        null=True,
        blank=True,
        validators=[DecimalValidator],
        help_text="Максимально доступное количество товара",
    )
    count = models.CharField(
        null=False,
        blank=False,
        validators=[DecimalValidator],
        help_text="Количество товара в заказе",
    )
    label = models.CharField(
        max_length=2048,
        null=True,
        blank=True,
        help_text='Название единиц измерения, например "кг" или "шт"',
    )

    def __str__(self):
        if self.label is not None:
            return f"{self.count} {self.label}"
        return self.count


class RenderedCartItem(models.Model):
    description = models.CharField(
        max_length=2048, null=True, blank=True, help_text="Описание товара"
    )
    discountedUnitPrice = models.CharField(
        null=True,
        blank=True,
        validators=[DecimalValidator],
        help_text="Цена за единицу товара с учётом скидок на позицию",
    )
    productId = models.UUIDField(
        max_length=2048,
        null=False,
        blank=False,
        help_text="Id товара в системе продавца. "
        "В параметрах запроса каждый идентификатор товара productId должен быть уникальным",
    )
    quantity = models.OneToOneField(
        ItemQuantity,
        on_delete=models.CASCADE,
        related_name="quantity",
        help_text="Количество товара в заказе",
    )
    subtotal = models.CharField(
        null=True,
        blank=True,
        validators=[DecimalValidator],
        help_text="Суммарная цена за позицию без учета скидок",
    )
    title = models.CharField(
        max_length=2048, null=False, blank=False, help_text="Наименование товара"
    )
    total = models.CharField(
        null=False,
        blank=False,
        validators=[DecimalValidator],
        help_text="Суммарная цена за позицию с учётом скидок на позицию",
    )

    def __str__(self):
        return f"{self.title} -- {self.quantity}"


class CartTotal(models.Model):
    amount = models.CharField(
        null=False,
        blank=False,
        validators=[DecimalValidator],
        help_text="Стоимость корзины с учетом всех скидок, и без учета доставки",
    )
    label = models.CharField(null=True, blank=True, max_length=2048)


class RenderedCart(models.Model):
    externalId = models.UUIDField(
        max_length=2048, help_text="Переданный продавцом идентификатор корзины"
    )
    items = ArrayField(RenderedCartItem, null=False, blank=False)
    total = models.OneToOneField(CartTotal, on_delete=models.CASCADE)
