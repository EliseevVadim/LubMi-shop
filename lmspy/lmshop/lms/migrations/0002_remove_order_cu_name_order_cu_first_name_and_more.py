# Generated by Django 4.2.9 on 2024-03-03 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cu_name',
        ),
        migrations.AddField(
            model_name='order',
            name='cu_first_name',
            field=models.CharField(default='first-name', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='cu_last_name',
            field=models.CharField(default='last-name', max_length=150),
            preserve_default=False,
        ),
    ]
