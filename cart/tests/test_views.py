from django.test import TestCase
from django.urls import reverse
from products.models import Product, Category
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
        
class RemoveFromCartViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Vinyl")
        self.product = Product.objects.create(
            name="Test Vinyl",
            slug="test-vinyl",
            category=self.category,
            price=Decimal("14.99"),
            stock=5
        )

        session = self.client.session
        session['cart'] = {
            str(self.product.id): {
                'quantity': 2,
                'price': str(self.product.price),
                'name': self.product.name
            }
        }
        session.save()

    def test_remove_product_from_cart(self):
        response = self.client.get(reverse('cart:remove_from_cart', args=[self.product.id]))
        self.assertRedirects(response, reverse('cart:view_cart'))
        cart = self.client.session.get('cart', {})
        self.assertNotIn(str(self.product.id), cart)

    def test_remove_nonexistent_product_does_not_error(self):
        response = self.client.get(reverse('cart:remove_from_cart', args=[999]))
        self.assertRedirects(response, reverse('cart:view_cart'))
        cart = self.client.session.get('cart', {})
        self.assertEqual(len(cart), 1)  # original item still there

class ViewCartContextTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Vinyl")
        self.product1 = Product.objects.create(
            name="Album A",
            slug="album-a",
            category=self.category,
            price=Decimal("9.99"),
            stock=5
        )
        self.product2 = Product.objects.create(
            name="Album B",
            slug="album-b",
            category=self.category,
            price=Decimal("14.50"),
            stock=3
        )

        session = self.client.session
        session['cart'] = {
            str(self.product1.id): {
                'quantity': 2,
                'price': str(self.product1.price),
                'name': self.product1.name
            },
            str(self.product2.id): {
                'quantity': 1,
                'price': str(self.product2.price),
                'name': self.product2.name
            }
        }
        session.save()

    def test_cart_view_context_totals(self):
        response = self.client.get(reverse('cart:view_cart'))
        self.assertEqual(response.status_code, 200)
        cart_items = response.context['cart_items']
        total = response.context['total']

        self.assertEqual(len(cart_items), 2)

        item1 = next(item for item in cart_items if item['id'] == str(self.product1.id))
        item2 = next(item for item in cart_items if item['id'] == str(self.product2.id))

        self.assertEqual(item1['quantity'], 2)
        self.assertEqual(item1['price'], self.product1.price)
        self.assertEqual(item1['subtotal'], Decimal("19.98"))

        self.assertEqual(item2['quantity'], 1)
        self.assertEqual(item2['price'], self.product2.price)
        self.assertEqual(item2['subtotal'], Decimal("14.50"))

        self.assertEqual(total, Decimal("34.48"))
