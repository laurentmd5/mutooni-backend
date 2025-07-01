# core/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include

# Importer les modules, pas directement les classes pour éviter les erreurs d'import
from core.views import stock, vente, achat, rh, transaction

router = DefaultRouter()

# Stock
router.register(r'categories', stock.CategorieProduitViewSet, basename='categorie')
router.register(r'produits', stock.ProduitViewSet, basename='produit')
router.register(r'mouvements', stock.MouvementStockViewSet, basename='mouvement')

# Ventes
router.register(r'clients', vente.ClientViewSet, basename='client')
router.register(r'ventes', vente.VenteViewSet, basename='vente')

# Achats
router.register(r'fournisseurs', achat.FournisseurViewSet, basename='fournisseur')
router.register(r'achats', achat.AchatViewSet, basename='achat')

# RH
router.register(r'employes', rh.EmployeViewSet, basename='employe')
router.register(r'salaires', rh.SalaireViewSet, basename='salaire')

# Transactions
router.register(r'transactions', transaction.TransactionViewSet, basename='transaction')

urlpatterns = [
    path("", include(router.urls)),
]
