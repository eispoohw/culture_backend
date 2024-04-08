from django.db import models
from django.core.validators import DecimalValidator
from utils.models import PreparedTitledModel, PreparedSluggedModel, PreparedTimedModel
from shop.db.models.product import Product, ProductCategory


class Size(PreparedSluggedModel):
    """ Размер единицы товара. """
    product_category = models.ForeignKey(
        ProductCategory,
        null=True,
        related_name='product_category_sizes',
        on_delete=models.CASCADE,
        help_text='Категория товаров для которой создан размер'
    )


class ProductUnit(PreparedTitledModel, PreparedTimedModel):
    """ Единица товара. """
    price = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        validators=[DecimalValidator],
        help_text='Цена товара'
    )
    size = models.ForeignKey(
        Size,
        related_name='product_units',
        on_delete=models.CASCADE,
        help_text='Размер единицы товара'
    )
    product = models.ForeignKey(Product, related_name='product_units', on_delete=models.CASCADE)
    reserved = models.BooleanField(default=False, null=False, help_text='Наличие брони')
