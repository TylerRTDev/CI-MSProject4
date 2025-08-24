from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from orders.models import Order
class AccountsViewTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser_01', password='pass1234')
    
    def test_login_view_get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_view_post_valid(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser_01',
            'password': 'pass1234'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'wrong',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")
    
    def test_order_history_view_requires_login(self):
        response = self.client.get(reverse('accounts:order_history'))
        self.assertEqual(response.status_code, 302)
    
    def test_order_history_view_logged_in(self):
        self.client.login(username='testuser_01', password='pass1234')
        response = self.client.get(reverse('accounts:order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/order_history.html')
        
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
        
    def test_change_password_view_requires_login(self):
        response = self.client.get(reverse('accounts:change_password'))
        self.assertEqual(response.status_code, 302)
    
    def test_account_detail_view_post_change_password_valid(self):
        self.client.force_login(self.user)
        post_data = {
            'change_password': '',
            'old_password': 'pass1234',
            'new_password1': 'NewPass1234!',
            'new_password2': 'NewPass1234!',
        }
        response = self.client.post(reverse('accounts:account_detail'), post_data)
        self.assertRedirects(response, reverse('accounts:account_detail'))
    
    def test_account_detail_view_post_change_password_invalid(self):
        self.client.force_login(self.user)
        post_data = {
            'change_password': '',
            'old_password': 'wrongpass',
            'new_password1': 'short',
            'new_password2': 'short',
        }
        response = self.client.post(reverse('accounts:account_detail'), post_data)
        self.assertRedirects(response, reverse('accounts:account_detail'))
    
    def test_logout_view_redirects(self):
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
    
    def test_update_email_view_redirects(self):
        response = self.client.get(reverse('accounts:update_email'))
        self.assertEqual(response.status_code, 302)
        
    def test_account_detail_view_requires_login(self):
        response = self.client.get(reverse('accounts:account_detail'))
        self.assertEqual(response.status_code, 302)
    
    def test_account_detail_view_logged_in(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('accounts:account_detail'))
        self.assertEqual(response.status_code, 302)
    
    def test_account_detail_view_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:account_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/account_detail.html')
        self.assertIn('profile_form', response.context)
        self.assertIn('password_form', response.context)
    
    def test_account_detail_view_post_update_profile_valid(self):
        self.client.force_login(self.user)
        post_data = {
            'update_profile': '',
            'username': 'newusername',
            'email': 'newemail@example.com',
            'old_password': 'pass1234',
            'new_password1': 'NewPass1234!',
            'new_password2': 'NewPass1234!',
        }
        response = self.client.post(reverse('accounts:account_detail'), post_data)
        self.assertRedirects(response, reverse('accounts:account_detail'))