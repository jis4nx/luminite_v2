import pytest
from rest_framework.parsers import json
from rest_framework.test import APIClient
from shop.models.product import Order, OrderItem
from shop.serializers import (
    UserProductSerializer,
)
from django.urls import reverse, reverse_lazy

client = APIClient()

""" Test for listing all product category"""


@pytest.mark.django_db
def test_lists_product_category():
    categories = client.get(reverse("category"))
    assert categories.status_code == 200


"""Test for create a new category for product """


@pytest.mark.django_db
def test_create_category():
    payload = dict(name="electronics")
    cat = client.post(reverse("category"), payload)
    assert cat.status_code == 201
    assert cat.data["name"] == payload["name"]


"""
Test For listing all product instances
"""


@pytest.mark.django_db
def test_list_product(new_product):
    product = client.get(reverse("product-list"))
    assert product.status_code == 200


"""
Test For Creating Product
"""


def test_create_product(new_product):
    product_data = UserProductSerializer(new_product).data
    product_data.pop("id")
    product_data["category"] = product_data["category"]["id"]
    res = client.post(reverse_lazy("product-list"), product_data, format="json")
    assert res.status_code == 201


"""
Test for creating new Product Item With Json Schema
"""


@pytest.mark.django_db
def test_product_item_json(new_product, product_item_factory_json, client):
    item = product_item_factory_json(
        product=new_product, attributes={"size": "S", "color": "Black"}
    )
    product = client.post(reverse("create-item"), item, format="multipart")

    assert product.status_code == 201


"""
Test if Product Item can be created with arbitrary Product Item Attributes

"""


def test_product_item_attribute(new_product, product_item_factory_json):
    item = product_item_factory_json(
        product=new_product, attributes={"size": "M", "space": 2}
    )
    product = client.post(reverse("create-item"), item, format="multipart")
    assert product.status_code == 400


"""
Test Order Item
"""


@pytest.mark.django_db(transaction=True)
def test_order_item(order_item_factory, product_itemA):
    order_item = order_item_factory(qty=2, items=[product_itemA])
    order = client.post(reverse("order"), order_item, format="json")
    assert order.status_code == 201
