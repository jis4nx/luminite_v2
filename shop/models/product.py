from django.contrib.auth import get_user_model
from django.db import models
from .choices import ProductSize, Colors, Status, DeliveryMethods


class Product(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    product_image = models.ImageField()

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=20, choices=ProductSize.choices)
    product_color = models.CharField(max_length=20, choices=Colors.choices)
    qty = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name


class ProductOrder(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    delivery_address = models.TextField()
    delivery_method = models.CharField(
        max_length = 20,
        choices=DeliveryMethods.choices
    )
    status = models.CharField(
        max_length = 20,
        choices=Status.choices,
        default=Status.PENDING
    )

    def __str__(self):
        return self.user.email
