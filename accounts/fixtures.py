import pytest
from accounts.models import User


@pytest.fixture()
def new_user(email="test@gmail.com", password="test@123123"):
    user = User.objects.create_user(email=email, password=password)
    return user


@pytest.fixture()
@pytest.mark.django_db
def user_factory():
    def create_new_user(
        email: str = "testuser@gmail.com",
        type: str = "CUSTOMER",
        password: str = "test@123",
        is_staff: bool = False,
        is_superuser: bool = False,
        is_active: bool = True,
    ):
        user = User.objects.create_user(
            email=email,
            type=type,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )

        return user

    return create_new_user
