from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.


currency_choice = (
    ('USD', 'USD'),
    ('RUB', 'RUB')
)

duration_choice = (
    ('once', 'once'),
    ('repeating', 'repeating'),
    ('forever', 'forever'),
)


class Item(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название продукта', null=False, blank=False)
    discription = models.TextField(verbose_name='Описание продукта')
    price = models.DecimalField(verbose_name='Цена', max_digits=12, decimal_places=2, validators=[MinValueValidator(0)],
                                null=False, blank=False)
    currency = models.CharField(max_length=3, choices=currency_choice)

    def __str__(self):
        return f"{self.name} : {self.price} {self.currency}"


class Discount(models.Model):
    name = models.CharField(max_length=64,verbose_name='Название купона')
    percent_off = models.IntegerField(verbose_name='Процент скидки')
    duration = models.CharField(max_length=16, choices=duration_choice, verbose_name='Длительность')
    duration_in_months = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(12)])

    def __str__(self):
        return self.name

class Order(models.Model):
    items = models.ManyToManyField(Item, verbose_name='Предметы в заказе')
    currency = models.CharField(max_length=3, choices=currency_choice)
    discounts = models.ManyToManyField(Discount, verbose_name='Купоны')

    def __str__(self):
        return f"Заказ - {self.id}"