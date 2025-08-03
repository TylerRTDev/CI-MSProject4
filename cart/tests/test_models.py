from django.test import TestCase
from decimal import Decimal
from django.contrib.auth.models import User
from products.models import Product, Category
from cart.models import CartItem

class CartItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='pass1234')
        cls.category = Category.objects.create(name="CD")
        cls.product = Product.objects.create(
            name="Sample Album",
            slug="sample-album",
            category=cls.category,
            price=Decimal('9.99'),
            stock=20
        )
        cls.cart_item = CartItem.objects.create(
            user=cls.user,
            product=cls.product,
            quantity=2
        )

    def test_cart_item_str_method(self):
        self.assertEqual(str(self.cart_item), "2 x Sample Album")

    def test_cart_item_total_price(self):
        expected = Decimal('19.98')
        self.assertEqual(self.cart_item.total_price(), expected)
        
    def test_cart_item_product_relation(self):
        self.assertEqual(self.cart_item.product.name, "Sample Album")

    def test_cart_item_user_relation(self):
        self.assertEqual(self.cart_item.user.username, "testuser")
