from django.test import TestCase
from django.urls import reverse
class AccountsViewTest(TestCase):
    
    def test_register_view_status_code(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/')

    def test_logged_in_user_can_access_profile(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)
    
    def test_logout_view_redirects(self):
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
    
    def test_update_email_view_redirects(self):
        response = self.client.get(reverse('accounts:update_email'))
        self.assertEqual(response.status_code, 302)
