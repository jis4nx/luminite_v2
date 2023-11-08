from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from shop.models.choices import PaymentMethod
from shop.models.product import Product, Category, ProductItem, ProductType, UserPayment
from shop.serializers import UserPaymentSerializer


@pytest.fixture
def user_sellerB(user_factory):
    user = user_factory(type="SELLER")
    return user


@pytest.fixture
def new_cat(db):
    cat = Category.objects.create(name="Men")
    return cat


@pytest.fixture
def new_product(db, new_cat, user_sellerB):
    product = Product.objects.create(
        owner=user_sellerB,
        name="Hoodie",
        desc="400% Unga Bunga Hoodie",
        category=new_cat,
        base_price=float(69.420),
    )
    return product


@pytest.fixture
def product_typeA(db):
    product_type = ProductType.objects.create(
        product_type="Cloth", attributes=["size", "color"]
    )
    return product_type


@pytest.fixture
@pytest.mark.django_db
def product_itemA(new_product):
    item = ProductItem.objects.create(
        product=new_product,
        image=SimpleUploadedFile(
            name="default.jpg",
            content=open("media/static/profile.png", "rb").read(),
            content_type="image/jpeg",
        ),
        price=float(500.0),
        attributes={"size": "M", "color": "Black"},
        qty_in_stock=10,
    )
    return item


@pytest.fixture
@pytest.mark.django_db
def new_payment(new_userA):
    payment = UserPayment.objects.create(
        user=new_userA.userprofile, payment_type=PaymentMethod.BKS, account_no="4934991"
    )
    return payment


@pytest.fixture
def product_item_factory_json(product_typeA):
    def create_product_item_json(
        product=new_product, qty=10, price=1500, attributes={}
    ):
        data = {
            "product_type": "Cloth",
            "price": price,
            "product": product.pk,
            "qty": qty,
            "attributes": attributes,
        }
        return data

    return create_product_item_json


@pytest.fixture()
def order_item_factory(new_payment, new_addressA, new_userA):
    def create_new_order_json(
        payment=new_payment,
        delivery_method="PTH",
        delivery_address=new_addressA,
        user=new_userA,
        items=[product_itemA],
        qty=2,
    ):
        order_data = {
            "order": {
                "payment": UserPaymentSerializer(payment).data,
                "delivery_method": delivery_method,
                "user": user.pk,
                "delivery_address": delivery_address.pk,
            },
            "items": [
                dict(product_item=item.pk, price=item.price, qty=qty) for item in items
            ],
        }
        return order_data

    return create_new_order_json
