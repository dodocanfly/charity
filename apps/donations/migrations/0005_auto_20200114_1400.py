# Generated by Django 3.0.2 on 2020-01-14 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0004_auto_20200114_1353'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='institutiontype',
            options={'ordering': ('type',), 'verbose_name': 'rodzaj instytucji', 'verbose_name_plural': 'rodzaj instytucji'},
        ),
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='institutions', to='donations.InstitutionType', verbose_name='rodzaj instytucji'),
        ),
    ]
