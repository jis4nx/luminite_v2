from .models.product import (
    Product,
    ProductItem,
    UserPayment,
    Category,
    Order,
    OrderItem,
)
from rest_framework import serializers
from rest_framework.response import Response


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="name", allow_null=True)

    class Meta:
        model = Category
        fields = ["category_name", "parent"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = ['name', 'desc', 'product_image']
        fields = "__all__"


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = ["product", "product_size",
                  "product_color", "qty_in_stock", "price"]

    def create(self, validated_data):
        product = self.validated_data['product']
        product_size = self.validated_data['product_size']
        product_color = self.validated_data['product_color']
        if ProductItem.objects.filter(
            product=product, product_size=product_size,
                product_color=product_color).exists():
            raise serializers.ValidationError("Product Item already exists!")
        product_item = ProductItem.objects.create(**validated_data)

        return product_item


class UserPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPayment
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    payment = UserPaymentSerializer()

    def create(slef, validated_data):
        payment_data = validated_data.pop("payment")
        payment_model = UserPayment.objects.create(**payment_data)
        shopcart = Order.objects.create(
            payment=payment_model, **validated_data)
        return shopcart


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"
