import pytest
from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import User
from shop.models.user import UserProfile, Address


class TestUserAccount(APITestCase):
    def setUp(self) -> None:
        self.register_url = reverse("register")
        self.user_data = {
            "email": "test@gmail.com",
            "password": "test123@123",
            "type": "OTHER",
            "password2": "test123@123",
        }

        self.res = self.client.post(reverse("register"), self.user_data, format="json")

        self.user = User.objects.all()
        self.user_profile = UserProfile.objects.all()

        """Create address for user profile object"""

        self.address = Address.objects.create(
            flat_no="1",
            street_no="one way",
            address_line1="420/69 one way",
            city="uganda",
            postal_code="69420H",
            user_profile=self.user_profile.first(),
        )
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_user_register_with_url(self):
        self.assertEqual(self.res.status_code, 201)

    def test_user_type(self):
        """Checks User type -> (OTHER, CUSTOMER, SELLER)"""
        self.assertEqual(self.user.first().type, "OTHER")
        self.assertEqual(self.user.count(), 1)

    def test_user_profile(self):
        """Test for User Profile object"""

        profile = self.user_profile.first()
        self.assertEqual(self.user_profile.count(), 1)
        self.assertEqual(profile.user.email, "test@gmail.com")
        self.assertEqual(profile.addresses.count(), 1)
        profile.save()

        """Check for address assignment to User Profile"""
        self.assertEqual(str(profile.addresses.first()), str(self.address))


@pytest.mark.django_db
def test_seller_account(user_sellerA):
    assert user_sellerA.type == "SELLER"
