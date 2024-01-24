# Generated by Django 4.2.9 on 2024-01-22 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0008_alter_product_article_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='article',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]