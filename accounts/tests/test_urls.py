from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts import views

class AccountsURLTest(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func, views.register_view)

    def test_profile_url_resolves(self):
        url = reverse('accounts:profile')
        self.assertEqual(resolve(url).func, views.profile_view)
