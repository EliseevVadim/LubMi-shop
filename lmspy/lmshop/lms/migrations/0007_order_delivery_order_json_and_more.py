# Generated by Django 4.2.13 on 2024-07-02 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0006_alter_availablesize_options_notificationrequest_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_order_json',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_supplements_json',
            field=models.TextField(blank=True, null=True),
        ),
    ]