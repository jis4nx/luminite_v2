import pytest
from rest_framework.test import APIClient
from shop.models.product import Category
from django.urls import reverse
client = APIClient()

""" Test for listing all product category"""


@pytest.mark.django_db
def test_lists_product_category():
    categories = client.get(reverse('category'))
    assert categories.status_code == 200


"""Test for create a new category for product """


@pytest.mark.django_db
def test_create_category():
    payload = dict(name="electronics")
    cat = client.post(reverse('category'), payload)
    assert cat.status_code == 201
    assert cat.data['name'] == payload['name']


"""
Test For listing all product instances
"""


@pytest.mark.django_db
def test_list_product(new_product):
    product = client.get(reverse('product-list'))
    assert product.status_code == 200


"""
Test for creating new Product Item
"""


@pytest.mark.django_db
@pytest.fixture
def test_product_item(new_product):
    payload = dict(
        product=new_product.id,
        product_size="S",
        product_color="RED",
        qty_in_stock="5",
        price=69.0

    )
    product = client.post(reverse('products'), payload)
    product_item = product.data
    assert product.status_code == 201
    return product_item
