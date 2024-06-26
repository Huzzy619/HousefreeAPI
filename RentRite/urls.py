from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("admin/", admin.site.urls),
    path("data-browser/", include("data_browser.urls")),
    path("api/v1/", include([
    path("accounts/", include("core.urls")),
    path("payments/", include("payments.urls")),
    path("chat/", include("chat.urls")),
    path("info/", include("info.urls")),
    path("", include("apartments.urls")),
    path("", include("notifications.urls")),
    path("", include("blog.urls")),
])),
    path("__debug__/", include("debug_toolbar.urls")),
]

# # Documentation paths

urlpatterns += [
    # YOUR PATTERNS
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-schema",
    ),
    path(
        "api/schema/redoc",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc-schema",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
