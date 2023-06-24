from unicodedata import name
from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("register", views.RegisterUser.as_view(), name="register"),
    path("token", views.CustomTokenPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify", views.VerifyToken.as_view(), name="token-verify"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile", views.ProfileView.as_view(), name="profile"),
    path("address", views.AddressView.as_view(), name="address"),
]
