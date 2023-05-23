from .models.product import (
    Product, ProductItem, UserPayment, Category, ShopCart, ShopCartItem
)
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='name', allow_null=True)

    class Meta:
        model = Category
        fields = ['category_name', 'parent']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        # fields = ['name', 'desc', 'product_image']
        fields = '__all__'


class ProductItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductItem
        fields = ['product', 'product_size', 'qty_in_stock', 'price']

    # def create(self, validated_data):
    #     product_data = validated_data.pop('product')
    #     product_model = Product.objects.create(**product_data)
    #     product_item = ProductItem.objects.create(
    #         product=product_model, **validated_data)
    #     return product_item


class UserPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPayment
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopCart
        fields = "__all__"

    payment = UserPaymentSerializer()

    def create(slef, validated_data):
        payment_data = validated_data.pop('payment')
        payment_model = UserPayment.objects.create(**payment_data)
        shopcart = ShopCart.objects.create(
            payment=payment_model, **validated_data
        )
        return shopcart


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopCartItem
        fields = "__all__"
