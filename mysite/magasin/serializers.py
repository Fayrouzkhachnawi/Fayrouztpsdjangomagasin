from rest_framework.serializers import ModelSerializer
from magasin.models import Produit
from magasin.models import Categorie

class ProduitSerializer(ModelSerializer):
 class Meta:
  model = Produit
  fields = ['libelle', 'prix', 'description']
class CategorySerializer(ModelSerializer):
 class Meta:
  model = Categorie
  fields = ['id', 'name', 'type_categorie']