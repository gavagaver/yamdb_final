from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    year = timezone.now().year
    if value > year:
        raise ValidationError(
            'Год произведения должен быть в прошлом.'
        )
    return value
