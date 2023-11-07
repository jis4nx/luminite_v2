from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from shop.models.product import Product, Category, ProductItem, ProductType


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
def product_itemA(db, new_product):
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
