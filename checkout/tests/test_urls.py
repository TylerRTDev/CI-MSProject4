from django.test import SimpleTestCase
from django.urls import reverse, resolve
from checkout import views
from django.urls import NoReverseMatch
from django.test import Client


class TestCheckoutURLs(SimpleTestCase):

    def test_checkout_url_resolves(self):
        url = reverse('checkout:checkout')
        self.assertEqual(resolve(url).func, views.checkout_view)
    
    def test_checkout_url_redirect_empty_cart(self):
        url = reverse('checkout:checkout')
        response = Client().get(reverse('checkout:checkout'))
        self.assertEqual(resolve(url).func, views.checkout_view)
        self.assertEqual(response.status_code, 302)  # Redirect due to empty cart
    
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
    
    def test_order_confirmation_missing_id_raises_error(self):
        with self.assertRaises(NoReverseMatch):
            reverse('checkout:order_confirmation')
    
    def test_checkout_namespace_reverse(self):
        url = reverse('checkout:checkout')
        self.assertEqual(url, '/checkout/')
    
    def test_create_checkout_session_disallows_get(self):
        response = Client().get(reverse('checkout:create_checkout_session'))
        self.assertEqual(response.status_code, 405)
    
    def test_order_confirmation_url_weird_id(self):
        url = reverse('checkout:order_confirmation', args=['weird$#id!!'])
        resolved_view = resolve(url).func
        self.assertEqual(resolved_view, views.order_confirmation)