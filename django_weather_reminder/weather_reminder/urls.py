from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

ROOT_API = "api"

schema_view = get_schema_view(
    openapi.Info(
        title="Weather Reminder",
        default_version='v1',
        description="API Documentation for support project",
        contact=openapi.Contact(email="foxkarasava55@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    permission_classes=[AllowAny],
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(f"{ROOT_API}/token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f"{ROOT_API}/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path(f"{ROOT_API}/subscriptions/", include(("subscriptions.urls", "subscriptions"), namespace="subscriptions")),
    path(f"{ROOT_API}/users/", include(("users.urls", "users"), namespace="users")),
    path(f"{ROOT_API}/", include((f"weather_api.urls", "weather_api"), namespace="weather_api")),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
