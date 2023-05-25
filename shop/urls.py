from django.urls import path
from . import views


urlpatterns = [
    path("", views.Index.as_view()),
    path("category/", views.CategoryView.as_view(), name="category"),
    path("product/", views.ProductView.as_view(), name="product"),
    path("products/", views.ProductItemView.as_view(), name="products"),
    path("order/", views.OrderItemView.as_view({'get': 'list'}), name="order"),
]
