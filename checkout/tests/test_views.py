from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from checkout.models import CheckoutOrder, CheckoutItem
from unittest.mock import patch
from django.conf import settings
from decimal import Decimal
import uuid

class CheckoutViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('checkout:create_checkout_session')
        unique_username = f"testuser_{uuid.uuid4().hex[:6]}"
        self.user = User.objects.create_user(username=unique_username, password='password123')
        self.cart_data = {
            '1': {
                'name': 'Test Product 1',
                'quantity': 2,
                'price': '10.00',
                'size': 'M'
            },
            '2': {
                'name': 'Test Product 2',
                'quantity': 1,
                'price': '20.00'
                # 'size' is optional (Omitted for this item)
            }
        }
        
        session = self.client.session
        session['cart'] = self.cart_data
        session.save()
        
        self.valid_form_data = {
            'email': 'test-email2@gmail.com',
            'full_name': 'Tyler K',
            'phone_number': '77700000',
            'shipping_address': '123 Fake Street',
            'shipping_city': 'Liverpool',
            'shipping_postcode': 'L1 0AP',
            'billing_address': '123 Fake Street',
            'billing_city': 'Liverpool',
            'billing_postcode': 'L1 0AP',
        }

    def test_checkout_view_get(self):
        response = self.client.get(reverse('checkout:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_checkout_view_redirects_if_cart_empty(self):
            session = self.client.session
            session['cart'] = {}
            session.save()
            response = self.client.get(reverse('checkout:checkout'))
            self.assertEqual(response.status_code, 302)
                        
    @patch('checkout.views.stripe.checkout.Session.create')
    def test_create_checkout_session_as_user_returns_200(self, mock_stripe_create):
        mock_stripe_create.return_value = {'id': 'cs_test_mocked123'}

        # Set up cart data in session
        session = self.client.session
        session['cart'] = {
            '1': {
                'product_id': 1,
                'quantity': 2,
                'size': 'M',
                'name': 'Test Product 1',
                'price': '10.00',
            },
            '2': {
                'product_id': 2,
                'quantity': 1,
                'size': None,
                'name': 'Test Product 2',
                'price': '20.00',
            },
        }
        session.save()

        form_data = {
            'email': 'test-email2@gmail.com',
            'full_name': 'Tyler K',
            'phone_number': '77700000',
            'shipping_address': '123 Fake Street',
            'shipping_city': 'Liverpool',
            'shipping_postcode': 'L1 0AP',
            'billing_address': '321 Fake Street',
            'billing_city': 'London',
            'billing_postcode': 'L5 5AP',
            'same_as_shipping': False
        }
        
        self.client.cookies.load({settings.SESSION_COOKIE_NAME: session.session_key})

        response = self.client.post(
            reverse('checkout:create_checkout_session'),
            data=form_data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())
        mock_stripe_create.assert_called_once()
    
    @patch('checkout.views.stripe.Webhook.construct_event')
    def test_webhook_creates_order(self, mock_construct_event):
        mock_event = {
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'id': 'cs_test_999',
                    'amount_total': 4000,
                    'metadata': {'user_id': str(self.user.id), 'cart': '{}'},
                    'email': 'guest@example.com',
                    'shipping_details': {'name': 'Guest User', 'address': {'city': 'London', 'postal_code': 'E1 6AN'}}
                }
            }
        }
        mock_construct_event.return_value = mock_event
        response = self.client.post(reverse('checkout:stripe_webhook'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CheckoutOrder.objects.filter(order_session='cs_test_999').exists())

    def test_order_success_view(self):
        order = CheckoutOrder.objects.create(
            order_session='cs_test_abc123',
            total_amount=Decimal('40.00'),
            full_name='User',
            email='user@example.com'
        )
        response = self.client.get(reverse('checkout:order_success') + f'?session_id={order.order_session}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order Confirmed')

    def test_order_confirmation_view(self):
        order = CheckoutOrder.objects.create(
            order_session='cs_test_abc123',
            total_amount=Decimal('40.00'),
            email='user@example.com',
            user=self.user
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse('checkout:order_confirmation', args=[order.order_session]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order.email)
    
    def test_order_confirmation_view_returns_404_for_invalid_order(self):
        invalid_order_id = 'nonexistent_session_id'
        response = self.client.get(reverse('checkout:order_confirmation', args=[invalid_order_id]))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'core/404.html')
    
    def test_stripe_webhook_invalid_signature_returns_400(self):
        payload = '{"id": "evt_test_invalid", "object": "event"}'
        sig_header = 'invalid_signature'

        with patch('stripe.Webhook.construct_event') as mock_construct_event:
            mock_construct_event.side_effect = ValueError("Invalid payload")

            response = self.client.post(
                reverse('checkout:stripe_webhook'),
                data=payload,
                content_type='application/json',
                **{'HTTP_STRIPE_SIGNATURE': sig_header}
            )

        self.assertEqual(response.status_code, 400)
    
    @patch('checkout.views.stripe.checkout.Session.create')
    def test_checkout_session_creation_exception_returns_500(self, mock_create_session):
        mock_create_session.side_effect = Exception("Stripe API failed")

        session = self.client.session
        session['cart'] = {
            '1': {'name': 'Test Product', 'quantity': 1, 'price': '10.00'}
        }
        session.save()

        form_data = {
            'email': 'test-email2@gmail.com',
            'full_name': 'Tyler K',
            'phone_number': '77700000',
            'shipping_address': '123 Fake Street',
            'shipping_city': 'Liverpool',
            'shipping_postcode': 'L1 0AP',
            'billing_address': '123 Fake Street',
            'billing_city': 'Liverpool',
            'billing_postcode': 'L1 0AP',
            'same_as_shipping': 'on',
        }

        response = self.client.post(
            reverse('checkout:create_checkout_session'),
            data=form_data
        )

        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], "Stripe API failed")
    
    
