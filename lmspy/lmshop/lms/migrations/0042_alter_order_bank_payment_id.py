# Generated by Django 4.2.9 on 2024-02-12 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0041_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='bank_payment_id',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
