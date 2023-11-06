from accounts.serializers import AddressSerializer
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
    """
    Serializer for Product Category
    """

    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "subcat", "parent")
        depth = 5

    def get_parent(self, obj):
        cats = []
        k = obj.parent
        if obj.parent:
            while k is not None:
                cats.append({"id": obj.parent.id, "name": obj.parent.name})
                k = k.parent
            return cats
        return None


class SimpleCategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "subcategories"]

    def get_subcategories(self, obj):
        subcategories = Category.objects.filter(parent=obj)
        if subcategories:
            return SimpleCategorySerializer(subcategories, many=True).data
        return []


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
        product = self.validated_data["product"]
        product_size = self.validated_data["product_size"]
        product_color = self.validated_data["product_color"]
        if ProductItem.objects.filter(
            product=product, product_size=product_size, product_color=product_color
        ).exists():
            raise serializers.ValidationError("Product Item already exists!")
        product_item = ProductItem.objects.create(**validated_data)

        return product_item

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["name"] = instance.product.name
        return rep


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

    payment = UserPaymentSerializer()

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        payment_data = validated_data.pop("payment")
        payment_model = UserPayment.objects.create(**payment_data)
        shopcart = Order.objects.create(payment=payment_model, **validated_data)
        return shopcart


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Order Items
    """

    class Meta:
        model = OrderItem
        fields = "__all__"


class MerchantOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["delivery_address"] = AddressSerializer(instance.delivery_address).data
        rep["total_cost"] = instance.get_total_cost()
        return rep


class MerchantOrderItemSerializer(serializers.ModelSerializer):
    order = MerchantOrderSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["product_item"] = ProductItemSerializer(
            instance.product_item, context={"request": self.context["request"]}
        ).data
        return rep
