from rest_framework import serializers
from .models import Currency, ExchangeRate


class ExchangeRatesSerializer(serializers.ModelSerializer):
    currency_code = serializers.CharField(source='currency.currency_code')

    class Meta:
        model = ExchangeRate
        fields = '__all__'
