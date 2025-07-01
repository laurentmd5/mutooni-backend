from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, PingView   # ← IMPORT OBLIGATOIRE

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),          # CRUD /api/users/
    path("ping/", PingView.as_view(), name="ping"),  # /api/ping/
]
