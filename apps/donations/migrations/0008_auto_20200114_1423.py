# Generated by Django 3.0.2 on 2020-01-14 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0007_auto_20200114_1411'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='institutiontype',
            options={'ordering': ('name',), 'verbose_name': 'rodzaj instytucji', 'verbose_name_plural': 'rodzaj instytucji'},
        ),
        migrations.RenameField(
            model_name='institutiontype',
            old_name='type',
            new_name='name',
        ),
    ]
