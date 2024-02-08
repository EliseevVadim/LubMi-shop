# Generated by Django 4.2.9 on 2024-02-08 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0036_city_city_lc'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='city',
            name='lms_city_city_19f7a8_idx',
        ),
        migrations.AddIndex(
            model_name='city',
            index=models.Index(fields=['city_lc', 'city'], name='lms_city_city_lc_5cf9b4_idx'),
        ),
    ]
