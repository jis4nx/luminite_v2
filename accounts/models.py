from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from .managers import UserManager


class UserType(models.TextChoices):
    CUSTOMER = "CUSTOMER", "Customer"
    SELLER = "SELLER", "Seller",
    OTHER = "OTHER", "Other"


class User(AbstractUser):
    objects = UserManager()

    username = None
    email = models.EmailField(_("Email address"), unique=True)

    # base_type = UserType.OTHER

    type = models.CharField(
        max_length=20, choices=UserType.choices, default=UserType.OTHER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.type = self.base_type
    #         return super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_type_valid",
                check=models.Q(type__in=["CUSTOMER", "SELLER", "OTHER"]),
            )
        ]


class CustomerManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=UserType.CUSTOMER)


class SellerManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=UserType.SELLER)


class Customer(User):
    base_type = "CUSTOMER"
    objects = CustomerManager()

    class Meta:
        proxy = True


class Seller(User):
    base_type = "SELLER"
    objects = SellerManager()

    class Meta:
        proxy = True
