# Generated by Django 4.2.13 on 2025-01-20 10:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0011_stuffaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pack_height',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Высота упаковки, см'),
        ),
        migrations.AddField(
            model_name='product',
            name='pack_length',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Длина упаковки, см'),
        ),
        migrations.AddField(
            model_name='product',
            name='pack_width',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Ширина упаковки, см'),
        ),
        migrations.AlterField(
            model_name='availablesize',
            name='size',
            field=models.CharField(max_length=30),
        ),
    ]
