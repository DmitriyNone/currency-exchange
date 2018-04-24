from django.db import models
from model_utils import Choices

CURRENCIES = Choices(
    ('USD', 'United States Dollars'),
    ('EUR', 'Euro'),
    ('CZK', 'Czech Republic Koruna'),
    ('PLN', 'Polish Zloty'),
)


class Currency(models.Model):
    currency_code = models.CharField(max_length=3, choices=CURRENCIES, default=CURRENCIES.USD, unique=True)


class ExchangeRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    timestamp = models.IntegerField(default=0)
    rate = models.DecimalField(max_digits=20, decimal_places=10)

