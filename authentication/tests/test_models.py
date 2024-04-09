from rest_framework.test import APITestCase
from authentication.models import User

class TestModel(APITestCase):

    def test_creates_user(self):
        user=User.objects.create_user('testuser', 'testuser@email.com', 'password123!')
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertFalse(user.is_staff)

    def test_creates_super_user(self):
        user=User.objects.create_superuser('testuser', 'testuser@email.com', 'password123!')
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertTrue(user.is_staff)

    def test_raises_error_when_no_username_is_provided(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username='', email='testuser@email.com', password='password123!')

    def test_raises_error_when_no_email_is_provided(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username='testuser', email='', password='password123!')

    def test_cant_create_super_user_with_no_is_staff_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser(
                username='testuser', email='testuser@email.com', password='password123!@', is_staff=False)

    def test_cant_create_super_user_with_no_super_user_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            User.objects.create_superuser(
                username='testuser', email='testuser@email.com', password='password123!@', is_superuser=False)
