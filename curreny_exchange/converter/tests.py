from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, APIClient, RequestsClient

# Create your tests here.


class GenerationTests(APITestCase):
    """
    Check that rates page is available
    """
    def test_check_rates_are_avaiable(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1/rates/')
        assert response.status_code == 200

    def test_check_all_currencies_are_present(self):
        response = self.client.get('http://127.0.0.1/rates/', format='json')
