from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from utils.models import PreparedSluggedModel, PreparedTimedModel
from colorfield.fields import ColorField
from django.utils.text import slugify


class Material(PreparedSluggedModel):
    """ Материал из которого сделан товар. """
    pass


class ProductCategory(PreparedSluggedModel):
    """ Категория товара. """
    parent_category = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )


class Color(PreparedSluggedModel):
    """ Цвет товара. """
    color = ColorField(format="hexa", null=False, blank=False, unique=True, help_text='HEX-код цвета')


class Product(PreparedSluggedModel, PreparedTimedModel):
    """ Товар. """
    title = models.CharField(max_length=128, null=False, blank=False, help_text='Название')
    article = models.CharField(max_length=128, primary_key=True, null=False, blank=False, help_text='Артикул')
    description = models.TextField(null=True, blank=True, help_text='Описание товара')

    materials = models.ManyToManyField(
        Material, related_name='products', through='ProductMaterials', null=True, help_text='Материал(ы) товара'
    )
    colors = models.ManyToManyField(Color, related_name='products', null=True, help_text='Цвет(а) товара')
    category = models.ForeignKey(
        ProductCategory, related_name='products', on_delete=models.CASCADE, help_text='Категория товара'
    )

    def __str__(self):
        return f"[{self.article}] {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.article)
        super().save(*args, **kwargs)


class ProductMaterials(models.Model):
    """ Процентный состав материала в товаре. Например, 70% хлопок, 30% полиэластан. """
    product = models.ForeignKey(Product, related_name='product_materials', on_delete=models.SET_NULL)
    material = models.ForeignKey(Material, related_name='product_materials', on_delete=models.SET_NULL)
    percentage = models.IntegerField(
        null=True, validators=[MinValueValidator(1), MaxValueValidator(100)], help_text='Количество в процентах'
    )


class ProductImage(models.Model):
    """ Изображение товара. """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cultureshop/items')
