from django.db import models
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Institution(models.Model):
    TYPE_CHOICES = (
        (1, 'fundacja'),
        (2, 'organizacja pozarządowa'),
        (3, 'zbiórka lokalna'),
    )
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1024, null=True, blank=True)
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=1)
    categories = models.ManyToManyField(Category, related_name=_('institutions'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Donation(models.Model):
    quantity = models.SmallIntegerField()

    # categories (relacja ManyToMany do modelu Category)
    # institution (klucz obcy do modelu Institution)
    # address (ulica plus numer domu)
    # phone_number (numer telefonu)
    # city
    # zip_code
    # pick_up_date
    # pick_up_time
    # pick_up_comment
    # user (klucz obcy do tabeli user; domyślna tabela zakładana przez django; może być Nullem, domyślnie Null).
