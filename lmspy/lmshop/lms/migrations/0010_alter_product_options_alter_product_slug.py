# Generated by Django 4.2.9 on 2024-01-22 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0009_alter_product_article_alter_product_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={},
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(editable=False, max_length=200, unique=True),
        ),
    ]
