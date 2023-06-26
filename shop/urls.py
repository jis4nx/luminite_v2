from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'product', views.ProductView, basename='product')

urlpatterns = [
    path("", views.Index.as_view()),
    path("", include(router.urls)),
    path("category/", views.CategoryView.as_view(), name="category"),
    path("products/", views.ProductItemView.as_view(), name="products"),
    path("product-attr/", views.ProductAttributeView.as_view(), name="product-attr"),
    path("order/", views.OrderItemView.as_view(), name="order"),
]
