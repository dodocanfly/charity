from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=254, verbose_name='adres e-mail', unique=True)
    first_name = models.CharField(max_length=30, verbose_name='imię')
    last_name = models.CharField(max_length=150, verbose_name='nazwisko')
    city = models.CharField(max_length=50, verbose_name='miejscowość', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('użytkownik')
        verbose_name_plural = _('użytkownicy')
