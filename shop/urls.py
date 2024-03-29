from django.urls import include, path
from rest_framework import routers
from shop.views import user_views, merchant_views

router = routers.DefaultRouter()
router.register(r"product", user_views.ProductView, basename="product")


merchant_urls = [
    path("list-orders/", merchant_views.ListOrders.as_view(), name="merchant-orders"),
    path(
        "merchant-products/",
        merchant_views.MerchantProducts.as_view(),
        name="merchant-products",
    ),
    path(
        "product-types/", merchant_views.GetProductTypes.as_view(), name="product-types"
    ),
    path(
        "merchant-items/",
        merchant_views.ListProductItems.as_view(),
        name="merchant-items",
    ),
    path(
        "merchant-products/<int:pk>",
        merchant_views.GetMerchantProduct.as_view(),
        name="merchant-product",
    ),
    path("item/", merchant_views.CreateItemView.as_view(), name="create-item"),
    path("merchant-product-items/<int:pk>", merchant_views.ListProductItems.as_view()),
    path("merchant-product-item/<int:pk>", merchant_views.GetItemView.as_view()),
    path("merchant-analytics/", merchant_views.MerchantAnalytics.as_view()),
]

urlpatterns = [
    path("", user_views.Index.as_view()),
    path("", include(router.urls)),
    path("category/", user_views.CategoryView.as_view(), name="category"),
    path("product/<int:pk>", user_views.ProductRetrieveView.as_view(), name="product"),
    path("item/<int:pk>", user_views.ShopItemRetrieveView.as_view(), name="items"),
    path(
        "product-attr/", user_views.ProductAttributeView.as_view(), name="product-attr"
    ),
    path("order/", user_views.OrderItemCreateView.as_view(), name="order"),
    path("items/", user_views.ShopItemView.as_view(), name="items"),
    path("user-orders/", user_views.GetUserOrders.as_view(), name="items"),
    path("invoice/<int:orderId>", user_views.GetInvoicePDF.as_view(), name="invoice"),
    path("search", user_views.SearchProduct.as_view(), name="search-product"),
    path("filter-item", user_views.ProductItemFilter.as_view(), name="search-product"),
    path("reviews", user_views.UserReview.as_view(), name="user-review"),
    path(
        "reviews/<int:pk>",
        user_views.RetrieveUserReview.as_view(),
        name="get-user-review",
    ),
    path("simple", user_views.SimpleView.as_view()),
] + merchant_urls
