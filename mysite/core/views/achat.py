from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Fournisseur, Achat
from core.serializers import FournisseurSerializer, AchatSerializer

class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nom","telephone","email"]

class AchatViewSet(viewsets.ModelViewSet):
    queryset = Achat.objects.select_related("fournisseur").prefetch_related("lignes__produit")
    serializer_class = AchatSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["statut","fournisseur"]
    search_fields = ["id"]
