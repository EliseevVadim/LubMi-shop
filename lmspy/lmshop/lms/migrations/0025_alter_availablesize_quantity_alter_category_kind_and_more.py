# Generated by Django 4.2.9 on 2024-01-31 14:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0024_order_cu_confirm_alter_order_cu_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availablesize',
            name='quantity',
            field=models.BigIntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='category',
            name='kind',
            field=models.CharField(choices=[('pt', 'Таксономия продуктов')], default='pt', max_length=2),
        ),
        migrations.AlterField(
            model_name='product',
            name='sales_quantity',
            field=models.BigIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
