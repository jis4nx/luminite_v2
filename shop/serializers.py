from accounts.serializers import AddressSerializer
from .models.product import (
    Product,
    ProductItem,
    Review,
    UserPayment,
    Category,
    Order,
    OrderItem,
    ProductType,
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


class UserProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["category"] = dict(name=instance.category.name, id=instance.category.id)
        rep["total_items"] = instance.product_items.count()
        return rep


class MerchantProductItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Product Item Object
    """

    product_id = serializers.IntegerField()
    product_type = serializers.CharField()

    class Meta:
        model = ProductItem
        fields = [
            "qty_in_stock",
            "price",
            "attributes",
            "product_id",
            "product_type",
            "image",
        ]

    def create(self, validated_data):
        productKey = self.validated_data["product_id"]
        qty = self.validated_data["qty_in_stock"]
        price = self.validated_data["price"]
        attributes = self.validated_data["attributes"]
        productType = self.validated_data["product_type"]
        product_type = ProductType.objects.get(product_type=productType)
        product = Product.objects.get(id=productKey)
        if self.instance is None:
            product_item = ProductItem.objects.create(
                product=product,
                qty_in_stock=qty,
                price=price,
                attributes=attributes,
                product_type=product_type,
                image=self.validated_data["image"],
            )
        return product_item

    def update(self, instance, validated_data):
        instance.qty_in_stock = validated_data.get(
            "qty_in_stock", instance.qty_in_stock
        )
        instance.attributes = validated_data.get("attributes", instance.attributes)
        instance.price = validated_data.get("price", instance.price)
        product_type = validated_data.get("product_type", instance.product_type)
        product = validated_data.get("product_id", instance.product.id)
        product_type = ProductType.objects.get(product_type=product_type)
        product = Product.objects.get(id=product)
        instance.product_type = product_type
        instance.product = product

        instance.save()
        return instance

    def validate(self, attrs):
        product_type = attrs.get("product_type")
        product_attrs = attrs.get("attributes")
        getType = ProductType.objects.get(product_type=product_type)
        product = attrs.get("product_id")
        if not Product.objects.filter(id=product).exists():
            return serializers.ValidationError("Product doesn't exist!")

        if getType and all(k in getType.attributes for k in product_attrs):
            return attrs
        raise serializers.ValidationError("Check Product Type & Attributes")


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, data):
        user = data.get("user")
        product_item = data.get("product_item")

        existing_reviews = Review.objects.filter(user=user, product_item=product_item)

        if existing_reviews.exists():
            raise serializers.ValidationError(
                "A review for this user and product item already exists!"
            )

        return data

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user_info = dict(
            image=instance.user.userprofile.image.url,
            name=instance.user.userprofile.full_name,
        )
        rep["user"] = user_info
        return rep


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        reviews = instance.item_reviews.all()
        review_serializer = ReviewSerializer(reviews, many=True)
        rep["name"] = instance.product.name
        rep["reviews"] = review_serializer.data
        rep["product_type"] = instance.product_type.product_type
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


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ("product_type", "attributes")
