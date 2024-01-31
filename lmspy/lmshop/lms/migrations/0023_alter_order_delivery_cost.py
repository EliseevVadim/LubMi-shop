# Generated by Django 4.2.9 on 2024-01-31 12:09

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0022_remove_order_product_remove_order_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_cost',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='RUR', max_digits=14),
        ),
    ]
