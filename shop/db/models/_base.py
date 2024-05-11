from django.core.validators import RegexValidator


def get_slug_kwargs(editable=True) -> dict:
    return {
        "editable": editable,
        "verbose_name": "Идентификатор на англ. языке",
        "max_length": 128,
        "unique": True,
        "validators": [
            RegexValidator(
                regex=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
                message="Неверный формат",
                code="invalid_slug",
            )
        ],
        "help_text": "Уникальный идентификатор на английском языке",
    }


def get_title_kwargs(is_unique=True) -> dict:
    return {
        "verbose_name": "Название",
        "max_length": 128,
        "null": False,
        "blank": False,
        "unique": is_unique,
        "help_text": "Уникальное название на русском языке",
    }
