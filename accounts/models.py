from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from .managers import UserManager


class User(AbstractUser):
    objects = UserManager()

    username = None
    email = models.EmailField(_("Email address"), unique=True)

    class Type(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        SELLER = "SELLER", "Seller"

    type = models.CharField(max_length=20, choices=Type.choices)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class CustomerManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Type.CUSTOMER)


class SellerManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Type.SELLER)


class Customer(User):
    objects = CustomerManager()

    class Meta:
        proxy = True


class Seller(User):
    objects = SellerManager()

    class Meta:
        proxy = True
