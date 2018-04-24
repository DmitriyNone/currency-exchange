from django.conf import settings
from django.db.models import Max
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.generics import GenericAPIView

from .models import ExchangeRate
from .serializers import ExchangeRatesSerializer
from .utils import update_rates, convert


class ViewRates(ReadOnlyModelViewSet):
    """
    Get currencies list and its rates
    """
    serializer_class = ExchangeRatesSerializer

    def get_queryset(self):
        timestamp = ExchangeRate.objects.aggregate(max_timestamp=Max('timestamp'))['max_timestamp']
        if not timestamp or timestamp < (datetime.now() - timedelta(days=1)).timestamp():
            update_rates(settings.REQUEST_ADDRESS)
            return ExchangeRate.objects.filter(timestamp=timestamp).all()
        else:
            return ExchangeRate.objects.filter(timestamp=timestamp)


class Convert(GenericAPIView):
    """
    Convert desired amount of currency
    """
    def get(self, request, *args, **kwargs):
        try:
            from_curr = kwargs['from_curr'].upper()
            to_curr = kwargs['to_curr'].upper()
            amount = kwargs['amount']
        except KeyError as ke:
            return Response(status=HTTP_400_BAD_REQUEST, exception="Argument is missing: {}".format(ke))

        try:
            amount = Decimal(amount)
        except InvalidOperation:
            return Response(status=HTTP_400_BAD_REQUEST, exception="Amount must be decimal")

        timestamp = ExchangeRate.objects.all().aggregate(max_timestamp=Max('timestamp'))['max_timestamp']
        from_rate = ExchangeRate.objects.get(timestamp=timestamp, currency__currency_code=from_curr).rate
        to_rate = ExchangeRate.objects.get(timestamp=timestamp, currency__currency_code=to_curr).rate

        result_amount = convert(from_rate, to_rate, amount)

        return Response(
            {'from currency': from_curr,
             'to currency': to_curr,
             'amount': amount,
             'result amount': result_amount
             },
            status=HTTP_200_OK
        )
