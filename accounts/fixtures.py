import pytest
from accounts.models import User
from shop.models.user import Address


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


@pytest.fixture
def user_sellerA(db, user_factory):
    user = user_factory(type="SELLER")
    return user


@pytest.fixture
def new_userA(db, user_factory):
    user = user_factory(email="testuser12@gmail.com")
    return user


@pytest.fixture
@pytest.mark.django_db
def new_addressA(new_userA):
    address = Address.objects.create(
        flat_no="04",
        street_no="3B One way",
        address_line1="45 Av",
        address_line2="",
        city="New York",
        postal_code="11000",
        user_profile=new_userA.userprofile,
    )
    return address
