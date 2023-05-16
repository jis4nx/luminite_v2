from django.contrib.auth import get_user_model
from django.db import models
from .choices import ProductSize, Colors, Status, DeliveryMethods, PaymentMethod
from .user import Address


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcat"
    )

    class Meta:
        verbose_name_plural = "categories"

    # Display Sub Categories with Top Level Categories

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return " -> ".join(full_path[::-1])


class Product(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    product_image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=20, choices=ProductSize.choices)
    product_color = models.CharField(max_length=20, choices=Colors.choices)
    qty_in_stock = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.product.name


class UserPayment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PaymentMethod.choices)
    account_no = models.CharField(max_length=255)


# Product ORDER Models


class ShopCart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    payment = models.ForeignKey(UserPayment, on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    delivery_method = models.CharField(
        max_length=20,
        choices=DeliveryMethods.choices
    )
    order_total_price = models.FloatField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class ShopCartItem(models.Model):
    cart = models.ForeignKey(ShopCart, on_delete=models.CASCADE)
    product = models.ForeignKey(
        ProductItem, on_delete=models.SET_NULL, null=True)
    qty = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
