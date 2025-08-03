from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile

class ProfileModelTest(TestCase):
    def test_profile_created_when_user_created(self):
        user = User.objects.create_user(username='signaltest', password='pass1234')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, Profile)
        self.assertEqual(user.profile.user.username, 'signaltest')