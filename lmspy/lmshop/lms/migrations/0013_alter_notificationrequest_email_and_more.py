# Generated by Django 4.2.9 on 2024-01-24 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0012_alter_notificationrequest_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationrequest',
            name='email',
            field=models.EmailField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='notificationrequest',
            name='phone',
            field=models.CharField(max_length=50, null=True),
        ),
    ]