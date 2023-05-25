from django.contrib.auth import get_user_model
from django.db import models
from .choices import ProductSize, Colors, Status, DeliveryMethods, PaymentMethod
from .user import Address
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=50, null=True)
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
        return " -> ".join(full_path)


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
    payment_type = models.CharField(
        max_length=20, choices=PaymentMethod.choices)
    account_no = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.payment_type}->{self.account_no}"


# Product ORDER Models


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    payment = models.ForeignKey(UserPayment, on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    delivery_method = models.CharField(
        max_length=20, choices=DeliveryMethods.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.user.email

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost


class OrderItem(models.Model):
    product = models.ForeignKey(
        ProductItem, on_delete=models.SET_NULL, null=True,
        related_name="order_items")
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')

    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.qty
