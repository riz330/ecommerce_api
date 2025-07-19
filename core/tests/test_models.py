from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@user.com',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@user.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@user.com',
            password='adminpass123'
        )
        self.assertEqual(admin.email, 'admin@user.com')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)