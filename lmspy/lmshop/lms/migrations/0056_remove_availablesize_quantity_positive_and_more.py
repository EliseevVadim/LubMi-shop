# Generated by Django 4.2.9 on 2024-02-17 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0055_orderitem_product'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='availablesize',
            name='quantity_positive',
        ),
        migrations.AddConstraint(
            model_name='availablesize',
            constraint=models.CheckConstraint(check=models.Q(('quantity__gte', 0)), name='quantity_no_negative'),
        ),
        migrations.AddConstraint(
            model_name='orderitem',
            constraint=models.CheckConstraint(check=models.Q(('quantity__gt', 0)), name='quantity_positive'),
        ),
    ]
