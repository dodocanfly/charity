# Generated by Django 3.0.2 on 2020-01-14 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donations', '0002_auto_20200113_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstitutionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=30, verbose_name='typ instytucji')),
            ],
            options={
                'verbose_name': 'typ instytucji',
                'verbose_name_plural': 'typy instytucji',
                'ordering': ('type',),
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'Kategoria', 'verbose_name_plural': 'Kategorie'},
        ),
        migrations.AlterModelOptions(
            name='donation',
            options={'ordering': ('-pick_up_date', '-pick_up_time'), 'verbose_name': 'darowizna', 'verbose_name_plural': 'darowizny'},
        ),
        migrations.AlterModelOptions(
            name='institution',
            options={'ordering': ('name',), 'verbose_name': 'Instytucja', 'verbose_name_plural': 'Instytucje'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='nazwa'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='address',
            field=models.CharField(max_length=250, verbose_name='ulica, nr budynku'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='categories',
            field=models.ManyToManyField(related_name='donations', to='donations.Category', verbose_name='kategorie'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='city',
            field=models.CharField(max_length=50, verbose_name='miejscowość'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='donations.Institution', verbose_name='instytucja'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='phone_number',
            field=models.CharField(max_length=50, verbose_name='numer telefonu'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pick_up_comment',
            field=models.TextField(max_length=1000, verbose_name='uwagi'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pick_up_date',
            field=models.DateField(verbose_name='data odbioru'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='pick_up_time',
            field=models.TimeField(verbose_name='godzina odbioru'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='quantity',
            field=models.SmallIntegerField(verbose_name='ilość'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='donations', to=settings.AUTH_USER_MODEL, verbose_name='darczyńca'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='zip_code',
            field=models.CharField(max_length=10, verbose_name='kod pocztowy'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='categories',
            field=models.ManyToManyField(related_name='institutions', to='donations.Category', verbose_name='kategorie'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='opis'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='name',
            field=models.CharField(max_length=100, verbose_name='nazwa'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.SmallIntegerField(choices=[(1, 'fundacja'), (2, 'organizacja pozarządowa'), (3, 'zbiórka lokalna')], default=1, verbose_name='rodzaj'),
        ),
    ]
