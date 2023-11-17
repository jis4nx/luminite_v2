from django.db import models
from django.contrib.postgres.fields import ArrayField
from accounts.models import Seller
from shop.models.managers import ProductItemManager

from .choices import (
    ColorChoices,
    ProductSize,
    Status,
    DeliveryMethods,
    PaymentMethod,
)
from .user import Address, UserProfile


class Category(models.Model):
    name = models.CharField(max_length=50, null=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcat"
    )

    class Meta:
        verbose_name_plural = "categories"

    # Display Sub Categories with Top Level Categories

    def __str__(self):
        return self.name
        # full_path = [self.name]
        # k = self.parent
        # while k is not None:
        #     full_path.append(k.name)
        #     k = k.parent
        # return " -> ".join(full_path)

    def get_all_subcategories(self):
        def collect_subcategories(category):
            subcategories = []

            for subcat in category.subcat.all():
                subcategories.append(collect_subcategories(subcat))

            if subcategories:
                return {
                    "category": category,
                    "subcategories": subcategories,
                }
            else:
                return {
                    "category": category,
                }

        return collect_subcategories(self)


class ProductType(models.Model):
    product_type = models.CharField(max_length=20, unique=True)
    attributes = ArrayField(models.CharField(max_length=100))

    def __str__(self):
        return self.product_type


class Product(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Seller, on_delete=models.CASCADE, default=4)
    desc = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    base_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_items"
    )
    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name="product_items"
    )
    product_size = models.CharField(
        max_length=20, choices=ProductSize.choices, null=True, blank=True
    )
    product_color = models.CharField(
        max_length=20,
        choices=ColorChoices.choices(),
        default=None,
        null=True,
        blank=True,
    )
    attributes = models.JSONField(default=dict)
    qty_in_stock = models.PositiveIntegerField()
    image = models.ImageField(default="static/no_image.jpg")
    price = models.FloatField()

    objects = ProductItemManager()

    def color_hex(self):
        return ColorChoices.color_code(self.product_color)

    def __str__(self):
        return self.product.name


class UserPayment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PaymentMethod.choices)
    account_no = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.payment_type}->{self.account_no}"


# Product ORDER Models


class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    payment = models.ForeignKey(UserPayment, on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    delivery_method = models.CharField(max_length=20, choices=DeliveryMethods.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Order #{self.id}"

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost

    @property
    def get_user_product_items(self):
        product_items = []
        for order_item in self.items.prefetch_related("product_item"):
            if order_item.product_item:
                product_items.append(order_item.product_item)
        return product_items


class OrderItem(models.Model):
    merchant_id = models.ForeignKey(
        Seller, on_delete=models.CASCADE, related_name="merchants"
    )
    product_item = models.ForeignKey(
        ProductItem, on_delete=models.SET_NULL, null=True, related_name="order_items"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.user}->{self.id}"

    def get_cost(self):
        return self.price * self.qty

    class Meta:
        ordering = ("-updated_at",)
