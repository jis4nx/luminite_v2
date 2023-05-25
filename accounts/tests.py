from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import User


class TestUserAccount(APITestCase):
    def setUp(self) -> None:
        self.register_url = reverse('register')
        self.user_data = {
            "email": "test@gmail.com",
            "password": "test123@123",
            "type": "OTHER",
            "password2": "test123@123"
        }

        self.res = self.client.post(
            reverse('register'), self.user_data, format="json")

    def test_user_register_with_url(self):
        self.assertEqual(self.res.status_code, 201)

    def test_user_type(self):
        user = User.objects.all()
        self.assertEqual(user.first().type, "OTHER")
        self.assertEqual(user.count(), 1)

