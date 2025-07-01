from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD complet sur le modèle User.

    - LIST & CREATE : réservés aux administrateurs (IsAdmin).
    - RETRIEVE / UPDATE / PARTIAL_UPDATE / DESTROY :
      l'utilisateur peut accéder/éditer *uniquement* son propre profil.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ("list", "create"):
            return [IsAdmin()]
        # Pour retrieve/update/destroy : l'utilisateur doit être connecté
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Limite la liste à l'utilisateur courant, sauf si admin.
        """
        user = self.request.user
        if user.is_authenticated and user.role == "admin":
            return super().get_queryset()
        return self.queryset.filter(id=user.id)

    def perform_create(self, serializer):
        """
        On force `is_active=True` par défaut,
        et any logique additionnelle au moment de la création.
        """
        serializer.save(is_active=True)


# ─────────────────────────────────────────────────────────────
# Endpoint de disponibilité API : /api/ping/
# ─────────────────────────────────────────────────────────────

class PingView(APIView):
    """
    Vue très simple pour vérifier que l'API répond.

    Accessible sans authentification (AllowAny).
    Renvoie {"ping": "pong"}.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Test de disponibilité de l'API",
        description="Renvoie « pong » afin de confirmer que l'API Mutooni est opérationnelle.",
        responses={200: {"type": "object", "properties": {"ping": {"type": "string"}}}},
    )
    def get(self, request):
        return Response({"ping": "pong"})
