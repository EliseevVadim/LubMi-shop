# Generated by Django 4.2.9 on 2024-02-17 19:05

import django.core.validators
from django.db import migrations
import djmoney.models.fields
import djmoney.money


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0053_availablesize_quantity_positive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='actual_price',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='RUR', max_digits=14, validators=[django.core.validators.MinValueValidator(djmoney.money.Money(0.01, currency='RUR'))]),
        ),
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='RUR', max_digits=14, null=True, validators=[django.core.validators.MinValueValidator(djmoney.money.Money(0.01, currency='RUR'))]),
        ),
    ]
