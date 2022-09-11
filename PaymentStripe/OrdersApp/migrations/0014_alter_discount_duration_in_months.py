# Generated by Django 4.1.1 on 2022-09-11 21:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrdersApp', '0013_alter_discount_duration_in_months_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='duration_in_months',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(12)]),
        ),
    ]
