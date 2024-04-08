from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify


class PreparedTitledModel(models.Model):
    """ Шаблонная модель с уникальным названием (title). """
    title = models.CharField(max_length=128, null=False, blank=False, unique=True, help_text='Название')

    def __str__(self):
        return self.title


class PreparedNonUniqueTitledModel(models.Model):
    """ Шаблонная модель с неуникальным названием (title). """
    title = models.CharField(max_length=128, null=False, blank=False, unique=False, help_text='Название')

    def __str__(self):
        return self.title


class PreparedSluggedModel(PreparedTitledModel):
    """ Шаблонная модель со слагом. """
    slug = models.CharField(
        max_length=128,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[a-z0-9]+(?:-[a-z0-9]+)*$',
            message='Неверный формат',
            code='invalid_slug'
        )],
        help_text='Идентификатор на английском языке'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PreparedTimedModel(models.Model):
    """ Шаблонная модель с датами создания и обновления. """
    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата обновления')
