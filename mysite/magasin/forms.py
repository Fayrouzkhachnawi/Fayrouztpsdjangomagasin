from django.forms import ModelForm
from .models import Produit
from .models import Fournisseur
from .models import Commande
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
class ProduitForm(ModelForm): 
    class Meta : 
     model = Produit 
     fields = "__all__" #pour tous les champs de la table
    #fields=['libelle','description'] #pour qulques champs
class FournisseurForm(ModelForm): 
    class Meta : 
     model = Fournisseur
     fields = "__all__" #pour tous les champs de la table
    #fields=['libelle','description'] #pour qulques champs
class CommandeForm(ModelForm): 
    class Meta : 
     model = Commande
     fields = ['dateCde', 'totalCde', 'produits'] #pour tous les champs de la table
    #fields=['libelle','description'] #pour qulques champs
    def __init__(self, *args, **kwargs):
        super(CommandeForm, self).__init__(*args, **kwargs)
        self.fields['produits'].queryset = Produit.objects.all()
class DeleteProduitForm(ModelForm):
    class Meta:
     model = Produit
     fields = ['id'] 
class UserRegistrationForm(UserCreationForm):
 first_name = forms.CharField(label='Prénom')
 last_name = forms.CharField(label='Nom')
 email = forms.EmailField(label='Adresse e-mail')
class Meta(UserCreationForm.Meta):
 model = User
 fields = UserCreationForm.Meta.fields + ('first_name', 'last_name' , 'email')

class MaCommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['dateCde', 'totalCde', 'produits']