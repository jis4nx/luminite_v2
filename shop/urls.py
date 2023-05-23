from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view()),
    path('category/', views.CategoryView.as_view(), name='category'),
    path('product/', views.ProductView.as_view(), name='product'),
    path('products/', views.ProductItemView.as_view(), name='products'),
    path('shop-cart/', views.ShopCartView.as_view(), name='cart'),
]
