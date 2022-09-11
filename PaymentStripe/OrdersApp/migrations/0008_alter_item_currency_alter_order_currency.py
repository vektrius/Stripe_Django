# Generated by Django 4.1.1 on 2022-09-11 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrdersApp', '0007_order_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('RUB', 'RUB')], max_length=3),
        ),
        migrations.AlterField(
            model_name='order',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('RUB', 'RUB')], max_length=3),
        ),
    ]