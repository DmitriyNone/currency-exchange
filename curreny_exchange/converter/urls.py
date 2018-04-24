from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import ViewRates, Convert

router = DefaultRouter()
router.register(r'rates', ViewRates, 'rates')

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^(?P<from_curr>.+)/(?P<to_curr>.+)/(?P<amount>.+)/&?', Convert.as_view(), name='currency-convert')
]