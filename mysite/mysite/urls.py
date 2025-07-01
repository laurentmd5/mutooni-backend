"""Point d’entrée URL racine du projet « mysite »."""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Redirection de la racine vers Swagger UI
    path("", RedirectView.as_view(url="/api/docs/", permanent=False)),

    # Interface d’administration Django
    path("admin/", admin.site.urls),

    # API REST principale (ex: core)
    path("api/", include("core.urls")),

    # API REST utilisateurs
    path("api/", include("users.urls")),  # ← AJOUT INDISPENSABLE

    # Authentification DRF (interface browsable API)
    path("api-auth/", include("rest_framework.urls")),

    # Documentation automatique avec drf-spectacular
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
