# Generated by Django 4.2.9 on 2024-01-28 16:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0014_telegrambot_alter_notificationrequest_ppk_chat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Param',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Имя', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Значение', models.CharField(max_length=250)),
                ('Описание', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='availablesize',
            options={'ordering': ['size']},
        ),
        migrations.AlterField(
            model_name='availablesize',
            name='size',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Размер не соответствует шаблону', regex='^(\\d*(?:M|X{0,2}[SL]))(?:$|\\s+.*$)')]),
        ),
        migrations.AddConstraint(
            model_name='availablesize',
            constraint=models.UniqueConstraint(fields=('size', 'product_id'), name='unique_size_per_product'),
        ),
    ]
