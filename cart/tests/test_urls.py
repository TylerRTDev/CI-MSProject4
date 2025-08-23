from django.test import SimpleTestCase
from django.urls import reverse, resolve
from cart import views


class CartUrlsTest(SimpleTestCase):
    def test_view_cart_url_resolves(self):
        url = reverse('cart:view_cart')
        self.assertEqual(resolve(url).func, views.view_cart)