from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('nazwa'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('Kategoria')
        verbose_name_plural = _('Kategorie')


class Institution(models.Model):
    TYPE_CHOICES = (
        (1, _('fundacja')),
        (2, _('organizacja pozarządowa')),
        (3, _('zbiórka lokalna')),
    )
    name = models.CharField(_('nazwa'), max_length=100)
    description = models.TextField(_('opis'), max_length=1000, null=True, blank=True)
    type = models.SmallIntegerField(_('rodzaj'), choices=TYPE_CHOICES, default=1)
    categories = models.ManyToManyField(Category, related_name='institutions', verbose_name=_('kategorie'))

    @property
    def categories_str(self):
        return ', '.join(self.categories.values_list('name', flat=True))

    @property
    def short_descr(self):
        return self.description[:150] + ('...' if len(self.description) > 153 else '')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('Instytucja')
        verbose_name_plural = _('Instytucje')


class Donation(models.Model):
    quantity = models.SmallIntegerField(_('ilość'))
    categories = models.ManyToManyField(Category, related_name='donations', verbose_name=_('kategorie'))
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='donations',
                                    verbose_name=_('instytucja'))
    address = models.CharField(_('ulica, nr budynku'), max_length=250)
    phone_number = models.CharField(_('numer telefonu'), max_length=50)
    city = models.CharField(_('miejscowość'), max_length=50)
    zip_code = models.CharField(_('kod pocztowy'), max_length=10)
    pick_up_date = models.DateField(_('data odbioru'))
    pick_up_time = models.TimeField(_('godzina odbioru'))
    pick_up_comment = models.TextField(_('uwagi'), max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='donations',
                             verbose_name=_('darczyńca'))

    def __str__(self):
        return f'{self.institution.name} - {self.pick_up_date} ({self.pick_up_comment[:15]}...)'

    class Meta:
        ordering = ('-pick_up_date', '-pick_up_time')
        verbose_name = _('darowizna')
        verbose_name_plural = _('darowizny')
