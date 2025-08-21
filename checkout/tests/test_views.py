from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from checkout.models import CheckoutOrder
from decimal import Decimal

class CheckoutViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.cart_data = {
            '1': {'quantity': 2, 'price': '10.00'},
            '2': {'quantity': 1, 'price': '20.00'}
        }
        session = self.client.session
        session['cart'] = self.cart_data
        session.save()

    def test_checkout_view_get(self):
        response = self.client.get(reverse('checkout:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
