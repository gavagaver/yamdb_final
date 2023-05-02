import uuid

from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    MODERATOR = 'moderator', 'Модератор'
    ADMIN = 'admin', 'Администратор'
    USER = 'user', 'Пользователь'


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=settings.MAX_LENGHT_USERNAME,
                                unique=True,
                                validators=[username_validator])
    email = models.EmailField(
        verbose_name='эл. почта',
        unique=True,
        blank=False)
    bio = models.TextField(
        max_length=settings.MAX_LENGHT_EMAIL,
        verbose_name='о себе',
        blank=True, null=True)
    role = models.CharField(
        max_length=settings.MAX_LENGHT_EMAIL,
        verbose_name='Роль',
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    first_name = models.CharField(null=True, blank=True,
                                  max_length=settings.MAX_LENGHT_FIRST_NAME)
    last_name = models.CharField(null=True, blank=True,
                                 max_length=settings.MAX_LENGHT_LAST_NAME)
    password = models.CharField(null=True, blank=True, max_length=150)

    is_active = models.BooleanField(default=True)
    # Свойство USERNAME_FIELD сообщает нам, какое поле мы будем использовать
    # для входа в систему. В данном случае мы хотим использовать почту.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    confirmation_code = models.TextField(default=uuid.uuid4, editable=False)

    @property
    def is_user(self):
        return self.role == UserRole.USER

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_admin(self):
        return (self.role == UserRole.ADMIN
                or self.is_staff
                or self.is_superuser)

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
