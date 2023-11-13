from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop.views.user_views import Index
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema-view"),
    path("admin/", admin.site.urls),
    path("shop/", include("shop.urls")),
    path("account/", include("accounts.urls")),
    path(
        "api/docs",
        SpectacularSwaggerView.as_view(url_name="schema-view"),
        name="api-docs",
    ),
    path(
        "api/redoc/", SpectacularRedocView.as_view(url_name="schema-view"), name="redoc"
    ),
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
