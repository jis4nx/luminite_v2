import pytest
from accounts.models import User


@pytest.fixture()
def new_user(email="test@gmail.com", password="test@123123"):
    user = User.objects.create_user(email=email,  password=password)
    return user
