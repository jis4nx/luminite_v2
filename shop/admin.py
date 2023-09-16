from django.contrib import admin
from .models.user import UserProfile, Address
from .models.product import (
    Category,
    ProductItem,
    Product,
    Order,
    OrderItem,
    UserPayment,
    ProductType
)
from django.contrib.admin import ModelAdmin


# Admin Interface
class ProductItemDisplay(ModelAdmin):
    list_display = ["product", "product_size", "product_color", "qty_in_stock"]
    list_filter = ["product_size"]


class ProductOrderDisplay(ModelAdmin):
    list_display = ["user", "product", "status"]


# Register Models
admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductItem, ProductItemDisplay)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserPayment)
admin.site.register(Address)
admin.site.register(ProductType)
