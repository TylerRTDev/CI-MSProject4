from django.test import TestCase
from django.urls import reverse
from products.models import Product, Category
from django.contrib.auth.models import User
from decimal import Decimal

class CartViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="CD")
        self.product = Product.objects.create(
            name="Session Test",
            slug="session-test",
            category=self.category,
            price=Decimal("9.99"),
            stock=10
        )
        self.session = self.client.session
        self.session['cart'] = {
            str(self.product.id): {
                'quantity': 1,
                'price': (str(self.product.price)),
                'name': self.product.name,
            }
        }
        self.session.save()

    def test_update_cart_quantity_increases(self):
        response = self.client.post(reverse('cart:update_cart'), {
            'item_id': Decimal(self.product.id),
            'quantity': 3
        })
        self.assertRedirects(response, reverse('cart:view_cart'))
        updated_cart = self.client.session['cart']
        self.assertEqual(updated_cart[str(self.product.id)]['quantity'], 3)

    def test_update_cart_quantity_removes_item(self):
        response = self.client.post(reverse('cart:update_cart'), {
            'item_id': str(self.product.id),
            'quantity': 0
        })
        self.assertRedirects(response, reverse('cart:view_cart'))
        updated_cart = self.client.session['cart']
        self.assertNotIn(str(self.product.id), updated_cart)
        
class AddToCartViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Vinyl")
        self.product = Product.objects.create(
            name="Test Vinyl",
            slug="test-vinyl",
            category=self.category,
            price=Decimal('14.99'),
            stock=10
        )

    def test_add_to_cart_initial(self):
        response = self.client.post(
            reverse('products:add_to_cart', args=[self.product.id]),
            data={'quantity': 1}
        )
        self.assertRedirects(response, reverse('products:detail', args=[self.product.slug]))
        cart = self.client.session['cart']
        self.assertIn(str(self.product.id), cart)
        self.assertEqual(cart[str(self.product.id)]['quantity'], 1)

    def test_add_to_cart_duplicate(self):
        # First add
        self.client.post(reverse('products:add_to_cart', args=[self.product.id]), data={'quantity': 1})

        # Add again
        self.client.post(reverse('products:add_to_cart', args=[self.product.id]), data={'quantity': 2})

        cart = self.client.session['cart']
        self.assertEqual(cart[str(self.product.id)]['quantity'], 3)

    def test_add_to_cart_redirect(self):
        response = self.client.post(
            reverse('products:add_to_cart', args=[self.product.id]),
            data={'quantity': 1}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('products:detail', args=[self.product.slug]))
