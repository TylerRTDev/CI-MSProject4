from django.test import SimpleTestCase
from django.urls import reverse, resolve
from checkout import views


class TestCheckoutURLs(SimpleTestCase):

    def test_checkout_url_resolves(self):
        url = reverse('checkout:checkout')
        self.assertEqual(resolve(url).func, views.checkout_view)
    
    def test_create_checkout_session_url_resolves(self):
        url = reverse('checkout:create_checkout_session')
        self.assertEqual(resolve(url).func, views.create_checkout_session)
        
    def test_order_success_url_resolves(self):
        url = reverse('checkout:order_success')
        self.assertEqual(resolve(url).func, views.order_success)
        
    def test_order_confirmation_url_resolves(self):
        url = reverse('checkout:order_confirmation', args=['123abc'])
        self.assertEqual(resolve(url).func, views.order_confirmation)
    
    def test_stripe_webhook_url_resolves(self):
        url = reverse('checkout:stripe_webhook')
        self.assertEqual(resolve(url).func, views.stripe_webhook)