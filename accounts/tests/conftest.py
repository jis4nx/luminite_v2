import pytest
from accounts.models import User


@pytest.fixture
def new_user():
    def create_test_user(email="test123@gmail.com", password="test@123"):
        user = User.objects.create_user(email=email,  password=password)
        return user
    return create_test_user
