from .models.product import (
    Product,
    ProductItem,
    UserPayment,
    Category,
    Order,
    OrderItem,
)
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="name", allow_null=True)

    class Meta:
        model = Category
        fields = ["category_name", "parent"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
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
    payment = UserPaymentSerializer()

    class Meta:
        model = Order
        fields = '__all__'

    def create(slef, validated_data):
        payment_data = validated_data.pop("payment")
        payment_model = UserPayment.objects.create(**payment_data)
        shopcart = Order.objects.create(
            payment=payment_model, **validated_data)
        return shopcart


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product_item', 'order', 'price', 'qty']

    order = OrderSerializer()

    def create(self, validated_data):
        order = validated_data['order']
        product = validated_data['product_item']
        price = validated_data['price']
        qty = validated_data['qty']
        order_item = OrderItem.objects.create(
            product_item=product,
            order=OrderSerializer.create(OrderSerializer(), order),
            price=price,
            qty=qty
        )
        return order_item
