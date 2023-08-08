from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'product', views.ProductView, basename='product')

urlpatterns = [
    path("", views.Index.as_view()),
    path("", include(router.urls)),
    path("category/", views.CategoryView.as_view(), name="category"),
    path("product/<int:pk>", views.ProductRetrieveView.as_view(), name="product"),
    path("item/<int:pk>", views.ShopItemRetrieveView.as_view(), name="items"),
    path("product-attr/", views.ProductAttributeView.as_view(), name="product-attr"),
    path("order/", views.OrderItemCreateView.as_view(), name="order"),
    path("items/", views.ShopItemView.as_view(), name="items"),
    path("user-orders/", views.GetUserOrders.as_view(), name="items"),
    path("invoice/<int:orderId>", views.GetInvoicePDF.as_view(), name="invoice"),


]
