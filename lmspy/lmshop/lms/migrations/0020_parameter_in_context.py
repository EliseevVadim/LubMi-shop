# Generated by Django 4.2.9 on 2024-01-29 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0019_alter_availablesize_options_alter_availablesize_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='in_context',
            field=models.BooleanField(default=True),
        ),
    ]