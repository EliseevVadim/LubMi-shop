# Generated by Django 4.2.9 on 2024-02-12 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0044_alter_order_bank_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='id',
            field=models.IntegerField(default=0),
        ),
    ]
