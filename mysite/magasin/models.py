from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.
class Categorie(models.Model):
    TYPE_CHOICES=[('Al','Alimentaire'), ('Mb', 'Meuble'),('Sn', 'Sanitaire'), ('Vs', 'Vaisselle'),
                 ('Vt','Vêtement'),('Jx', 'Jouets'),
                      ('Lg','Linge de Maison'),('Bj','Bijoux'),('Dc', 'Décor')]
    name=models.CharField(max_length=50 , default='Alimentaire') 
    type_categorie=models.CharField(max_length=2 ,choices=TYPE_CHOICES)


    def __str__(self):
      return self.name

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    email = models.EmailField()
    telephone = models.CharField(max_length=8)

    def __str__(self):
        return self.nom+''+ self.adresse+''+self.email+''+self.telephone

class Produit(models.Model):
    TYPE_CHOICES=[('fr','Frais'), ('cs', 'Conserve'),('em', 'emballé')]
    libelle=models.CharField(max_length=255)
    description=models.TextField()
    prix=models.DecimalField(max_digits=10,decimal_places=3,default=0.000)
    type=models.CharField(max_length=2,choices= TYPE_CHOICES,default='em')
    Img=models.ImageField(blank=True, upload_to='media/')
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True)
    def __str__(self):
      return self.libelle+""+ self.description+""+ str(self.prix)

class ProduitNC(Produit):
    duree_garantie = models.CharField(max_length=100)
    
    def __str__(self):
        return self.duree_garantie , self.Produit
class Commande(models.Model):
    dateCde = models.DateField(null=True, default=date.today)
    totalCde = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    produits = models.ManyToManyField(Produit)
    def __str__(self):
        return  str(self.dateCde)+''+ str(self.totalCde)
  
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)
    quantite = models.PositiveIntegerField(default=1)