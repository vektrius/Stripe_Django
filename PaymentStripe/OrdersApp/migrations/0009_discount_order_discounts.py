# Generated by Django 4.1.1 on 2022-09-11 12:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrdersApp', '0008_alter_item_currency_alter_order_currency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название купона')),
                ('percent_off', models.IntegerField(verbose_name='Процент скидки')),
                ('duration', models.CharField(choices=[('once', 'once'), ('repeating', 'repeating'), ('forever', 'forever')], max_length=16, verbose_name='Длительность')),
                ('duration_in_months', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(12)])),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='discounts',
            field=models.ManyToManyField(to='OrdersApp.discount', verbose_name='Купоны'),
        ),
    ]
