from django.urls import include, path
from rest_framework import routers
from shop.views import user_views,merchant_views

router = routers.DefaultRouter()
router.register(r"product", user_views.ProductView, basename="product")


merchant_urls = [
    path("list-orders/", merchant_views.ListOrders.as_view())
]

urlpatterns = [
    path("", user_views.Index.as_view()),
    path("", include(router.urls)),
    path("category/", user_views.CategoryView.as_view(), name="category"),
    path("product/<int:pk>", user_views.ProductRetrieveView.as_view(), name="product"),
    path("item/<int:pk>", user_views.ShopItemRetrieveView.as_view(), name="items"),
    path("item/", user_views.CreateItemView.as_view(), name="create-item"),
    path(
        "product-attr/", user_views.ProductAttributeView.as_view(), name="product-attr"
    ),
    path("order/", user_views.OrderItemCreateView.as_view(), name="order"),
    path("items/", user_views.ShopItemView.as_view(), name="items"),
    path("user-orders/", user_views.GetUserOrders.as_view(), name="items"),
    path("invoice/<int:orderId>", user_views.GetInvoicePDF.as_view(), name="invoice"),
    path("search", user_views.SearchProduct.as_view(), name="search-product"),
    path("filter-item", user_views.ProductItemFilter.as_view(), name="search-product"),
]+merchant_urls
