from unicodedata import name
from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("register", views.RegisterUser.as_view(), name="register"),
    path("token", views.CustomTokenPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", views.CustomRefreshTokenView.as_view(), name="token_refresh"),
    path("token/verify", views.VerifyToken.as_view(), name="token-verify"),
    path("token/expired", views.TokenExpiration.as_view(), name="token-expiration"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "change-password/<int:pk>",
        views.ChangePasswordView.as_view(),
        name="change-password",
    ),
    path("profile", views.ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>", views.ProfileUpdateView.as_view(), name="profile-update"),
    path("address", views.AddressView.as_view(), name="address"),
    path("checktype", views.CheckType.as_view(), name="checktype"),
    path("getaddress/<int:pk>", views.GetAddressView.as_view(), name="getaddress"),
]
