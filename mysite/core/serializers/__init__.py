from .base import (
    CategorieProduitSerializer, ProduitSerializer,
    ClientSerializer, FournisseurSerializer
)
from .vente import VenteSerializer, LigneVenteSerializer
from .achat import AchatSerializer, LigneAchatSerializer
from .stock import MouvementStockSerializer
from .rh import EmployeSerializer, SalaireSerializer
from .transaction import TransactionSerializer
