from django.test import SimpleTestCase
from django.urls import reverse, resolve

class HomePageTests(SimpleTestCase):
    
    def test_home_page_url_resolves(self):
        url = reverse('core:home')
        self.assertEqual(resolve(url).view_name, 'core:home')