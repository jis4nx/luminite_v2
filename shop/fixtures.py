import pytest
from shop.models.product import Product, Category


@pytest.fixture
def new_cat():
    cat = Category.objects.create(
        name="Electronics"
    )
    return cat


@pytest.fixture
def new_product(new_cat):
    product = Product.objects.create(
        name="Hoodie",
        desc="400% Unga Bunga Hoodie",
        product_image="static/image/default.jpg",
        category=new_cat,
        base_price=float(69.420)
    )
    return product
