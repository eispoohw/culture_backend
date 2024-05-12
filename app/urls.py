from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Culture Shop Backend",
        default_version="v1",
        description="",
        contact=openapi.Contact(email="eispoohw@yandex.ru"),
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser, ],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("shop.api.urls")),
    path(
        "docs/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
