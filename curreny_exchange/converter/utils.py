import requests
import json
from datetime import datetime, timedelta

from django.db.transaction import atomic

from .models import CURRENCIES, ExchangeRate, Currency


@atomic
def update_rates(address):
    all_rates = requests.get(address).json()

    for key in all_rates['rates'].keys():
        if key in CURRENCIES._db_values:
            currency, created = Currency.objects.update_or_create(currency_code=key)
            ExchangeRate.objects.create(
                currency_id=currency.id, timestamp=all_rates['timestamp'], rate=all_rates['rates'][key]
            )


def convert(from_rate, to_rate, amount):
    return (amount / from_rate) * to_rate


