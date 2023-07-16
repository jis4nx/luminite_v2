from .models.product import (
    Product,
    ProductItem,
    UserPayment,
    Category,
    Order,
    OrderItem,
)

from shop.models import choices
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Product Category
    """

    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'parent')

    def get_parent(self, obj):
        if obj.parent:
            return obj.parent.name
        return None


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product Object
    """
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Product Item Object
    """
    class Meta:
        model = ProductItem
        fields = "__all__"

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
    """
    Serializes users payment data
    """
    class Meta:
        model = UserPayment
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for User Orders
    """
    payment = UserPaymentSerializer(many=True)

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
    """
    Serializer for Order Items
    """

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
