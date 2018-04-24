from django.conf import settings
from django.db.models import Max
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.generics import GenericAPIView

from .models import ExchangeRate
from .serializers import ExchangeRatesSerializer
from .utils import update_rates, convert


class Custom404(GenericAPIView):
    def get(self, request):
        return Response(
            {'status_code': 404, 'error': 'Requested method was not found, please refer Readme.md for usage examples'},
            status=HTTP_404_NOT_FOUND
        )


class ViewRates(ReadOnlyModelViewSet):
    """
    Get currencies list and its rates
    """
    serializer_class = ExchangeRatesSerializer

    def get_queryset(self):
        timestamp = ExchangeRate.objects.aggregate(max_timestamp=Max('timestamp'))['max_timestamp']
        if not timestamp or timestamp < (datetime.now() - timedelta(days=1)).timestamp():
            update_rates(settings.REQUEST_ADDRESS)
            return ExchangeRate.objects.filter(timestamp=timestamp)
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
            return Response(
                {'Exception': 'Amount must be decimal'},
                status=HTTP_400_BAD_REQUEST,
                exception="Amount must be decimal"
            )

        timestamp = ExchangeRate.objects.all().aggregate(max_timestamp=Max('timestamp'))['max_timestamp']
        if not timestamp or timestamp < (datetime.now() - timedelta(days=1)).timestamp():
            update_rates(settings.REQUEST_ADDRESS)
        try:
            from_rate = ExchangeRate.objects.get(timestamp=timestamp, currency__currency_code=from_curr).rate
        except Exception:
            return Response(
                {'Exception': from_curr + ' currency is not supported.'},
                status=HTTP_400_BAD_REQUEST,
                exception=from_curr + ' currency is not supported.'
            )
        try:
            to_rate = ExchangeRate.objects.get(timestamp=timestamp, currency__currency_code=to_curr).rate
        except Exception:
            return Response(
                {'Exception': to_curr + ' currency is not supported.'},
                status=HTTP_400_BAD_REQUEST,
                exception=to_curr + ' currency is not supported.'
            )

        result_amount = convert(from_rate, to_rate, amount)

        return Response(
            {'from_currency': from_curr,
             'to_currency': to_curr,
             'amount': amount,
             'result_amount': result_amount
             },
            status=HTTP_200_OK
        )
