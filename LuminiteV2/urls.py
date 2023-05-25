from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)


urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema-view"),
    path("admin/", admin.site.urls),
    path("shop/", include("shop.urls")),
    path("account/", include("accounts.urls")),
    path("api/docs", SpectacularSwaggerView.as_view(url_name="schema-view"),
         name="api-docs")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
