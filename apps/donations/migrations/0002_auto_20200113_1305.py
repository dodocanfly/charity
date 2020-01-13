# Generated by Django 3.0.2 on 2020-01-13 12:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='institution',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('address', models.CharField(max_length=250)),
                ('phone_number', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=10)),
                ('pick_up_date', models.DateField()),
                ('pick_up_time', models.TimeField()),
                ('pick_up_comment', models.TextField(max_length=1000)),
                ('categories', models.ManyToManyField(related_name='donations', to='donations.Category')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='donations.Institution')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='donations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
