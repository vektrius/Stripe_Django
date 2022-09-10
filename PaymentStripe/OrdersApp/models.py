from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


currency_choise = (
    ('usd', 'USD'),
    ('rub', 'RUB')
)


class Item(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название продукта', null=False, blank=False)
    discription = models.TextField(verbose_name='Описание продукта')
    price = models.DecimalField(verbose_name='Цена', max_digits=12, decimal_places=2, validators=[MinValueValidator(0)],
                                null=False, blank=False)
    currency = models.CharField(max_length=3, choices=currency_choise)

    def __str__(self):
        return f"{self.name} : {self.price} {self.currency}"

class Order(models.Model):
    items = models.ManyToManyField(Item,verbose_name='Предметы в заказе')