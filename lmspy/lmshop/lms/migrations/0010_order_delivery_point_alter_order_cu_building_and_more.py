# Generated by Django 4.2.13 on 2024-07-23 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0009_alter_order_cu_apartment_alter_order_cu_entrance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_point',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='cu_building',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='cu_street',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_service',
            field=models.CharField(choices=[('cd', 'СДЭК (до двери)'), ('cp', 'СДЭК (ПВЗ)'), ('pr', 'Почта России')], default='cd', max_length=2),
        ),
    ]