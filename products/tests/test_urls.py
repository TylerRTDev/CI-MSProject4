from django.test import SimpleTestCase
from django.urls import reverse, resolve
from products import views

class ProductURLsTest(SimpleTestCase):
    def test_product_list_url_resolves(self):
        url = reverse('products:list')
        self.assertEqual(resolve(url).func, views.product_list)

    def test_product_detail_url_resolves(self):
        url = reverse('products:detail', kwargs={'slug': 'test-album'})
        self.assertEqual(resolve(url).func, views.product_detail)

    def test_add_to_cart_url_resolves(self):
        url = reverse('products:add_to_cart', kwargs={'product_id': 1})
        self.assertEqual(resolve(url).func, views.add_to_cart)
