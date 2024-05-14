from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import Produit
from .models import Fournisseur
from .models import Commande, Cart
from .forms import ProduitForm
from .forms import FournisseurForm, UserRegistrationForm, UserCreationForm, MaCommandeForm
from .forms import CommandeForm
from django.shortcuts import redirect
from .forms import DeleteProduitForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Sum, F
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime, timedelta
from plotly.offline import plot
import plotly.graph_objs as go
from django.db.models.functions import TruncMonth  # Import TruncMonth
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from magasin.models import Produit
from magasin.serializers import ProduitSerializer 
from magasin.models import Categorie
from magasin.serializers import CategorySerializer
from rest_framework import viewsets


def index(request):
    template = loader.get_template('magasin/mesProduits.html')
    products = Produit.objects.all()
    context = {'products': products}
    return render(request,'magasin/mesProduits.html', context) 


def fournisseur(request):
    template = loader.get_template('magasin/mesFournisseurs.html')
    fournis = Fournisseur.objects.all()
    context = {'fournis': fournis}
    return render(request,'magasin/mesFournisseurs.html', context) 


def commande(request):
    template = loader.get_template('magasin/mesCommandes.html')
    commands = Commande.objects.all()
    context = {'commands': commands}
    return render(request,'magasin/mesCommandes.html', context)

def indajout(request):
    if request.method == "POST" : 
     form = ProduitForm(request.POST,request.FILES)
     if form.is_valid():
        form.save()
        return render(request,'magasin/majProduits.html', {'form':form})
    else :
     form = ProduitForm() #créer formulaire vide
     return render(request,'magasin/majProduits.html',{'form':form})
def vitrineindex(request):
 template = loader.get_template('magasin/vitrine.html')
 list=Produit.objects.all()
 return render(request,'magasin/vitrine.html',{'list':list})


def nouveauFournisseur(request):
    if request.method == "POST" : 
     form = FournisseurForm(request.POST,request.FILES)
     if form.is_valid():
        form.save()
        return render(request,'magasin/nouveauFournisseur.html', {'form':form})
    else :
     form = FournisseurForm() #créer formulaire vide
     return render(request,'magasin/nouveauFournisseur.html',{'form':form})


def nouveauCommande(request):
    produits = Produit.objects.all() 
    if request.method == "POST":
       form = CommandeForm(request.POST, request.FILES)
       if form.is_valid():
            commande = form.save(commit=False)
            # Enregistrer la commande avant d'ajouter les produits
            commande.save()
            # Récupérer les produits associés à la commande depuis le formulaire
            produits = form.cleaned_data['produits']
            # Calculer le totalCde en fonction des produits associés à la commande
            total_cde = sum(produit.prix for produit in produits.all())
            for produit in produits:
                commande.produits.add(produit)
            commande.totalCde = total_cde
            

            # Enregistrer à nouveau la commande avec le totalCde mis à jour
            commande.save()
            return redirect('commande')
    else:
        form = CommandeForm()
    return render(request, 'magasin/majCommandes.html', {'form': form})
@login_required
def home(request):
 context={'val':"Menu Acceuil"}
 return render(request,'magasin/home.html',context)
def register(request):
 if request.method == 'POST' :
  form = UserCreationForm(request.POST)
  if form.is_valid():
   form.save()
   username = form.cleaned_data.get('username')
   password = form.cleaned_data.get('password1')
   user = authenticate(username=username, password=password)
   login(request,user)
   messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
   return redirect('home')
 else :
  form = UserCreationForm()
 return render(request,'registration/register.html',{'form' : form})
def add_to_cart(request, product_id):
    product = get_object_or_404(Produit, pk=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        produit=product
    )
    if not created:
        cart_item.quantite += 1
        cart_item.save()
    return redirect('cart')
def cart_view(request):
    # Récupérer tous les éléments du panier pour l'utilisateur connecté
    cart_items = Cart.objects.filter(user=request.user)
   
    total = cart_items.aggregate(total_price=Sum(F('produit__prix') * F('quantite')))['total_price'] or 0
    # Passer les éléments du panier à la template
    context = {
        'cart_items': cart_items,
        'total': total
    }

    return render(request, 'magasin/cart.html', context)
def update_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item.quantite = quantity
        cart_item.save()
    return redirect('cart')

stripe.api_key = settings.STRIPE_SECRET_KEY



def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        try:
            # Charge the customer using the payment token and amount
            charge = stripe.Charge.create(
                amount=request.POST['amount'],  # Amount in cents
                currency='usd',
                source=request.POST['stripeToken'],
                description='Payment for your order'
            )
            # Payment successful
            return JsonResponse({'success': True})
        except stripe.error.CardError as e:
            # If the card is declined
            return JsonResponse({'error': str(e)})
    else:
        # Handle GET requests (render the checkout form)
        return render(request, 'magasin/checkout.html')
def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    cart_item.delete()
    return render(request, 'magasin/cart.html')  # Redirect to the view cart page after deletion

def delete_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == 'POST':
        produit.delete()
        # Redirection vers une vue qui affiche une liste mise à jour des produits
        return redirect('index')
    return render(request, 'magasin/mesProduits.html')

def delete_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    if request.method == 'POST':
        fournisseur.delete()
        # Redirection vers une vue qui affiche une liste mise à jour des produits
        return redirect('fournisseur')
    return render(request, 'magasin/mesFournisseurs.html')

def delete_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == 'POST':
        commande.delete()
        # Redirection vers une vue qui affiche une liste mise à jour des produits
        return redirect('commande')
    return render(request, 'magasin/mesCommandes.html')

def update_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    form = CommandeForm(request.POST or None, instance=commande)
    
    # Calculer le totalCde en fonction des produits associés à la commande
    total_cde = 0
    for produit in commande.produits.all():
        total_cde += produit.prix  # Ajoutez le prix de chaque produit au total
        
    # Mettre à jour le champ totalCde dans la commande
    commande.totalCde = total_cde
    
    if form.is_valid():
        form.save()
        return redirect('commande')  # Redirige vers la vue détaillée de la commande mise à jour
    
    return render(request, 'magasin/update_commande.html', {'form': form, 'commande': commande})

def update_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    form = CommandeForm(request.POST or None, instance=commande)
    if form.is_valid():
        form.save()
        return redirect('commande')  # Redirige vers la vue détaillée de la commande mise à jour
    return render(request, 'magasin/update_commande.html', {'form': form, 'commande': commande})

def update_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    form = FournisseurForm(request.POST or None, instance=fournisseur)
    if form.is_valid():
        form.save()
        return redirect('fournisseur')  # Redirige vers la vue détaillée de la commande mise à jour
    return render(request, 'magasin/update_fournisseur.html', {'form': form, 'fournisseur': fournisseur})


def update_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('index')  # Rediriger vers la vue de détail du produit
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'magasin/update_produit.html', {'form': form, 'produit': produit})


def contact(request):
    return render(request, 'magasin/contact.html')


def plot_exampletwo(request):
    # Sample data for line chart
    revenue_data = Commande.objects.annotate(month=TruncMonth('dateCde')).values('month').annotate(revenue=Sum('totalCde'))
    months = [data['month'] for data in revenue_data]
    revenues = [data['revenue'] for data in revenue_data]
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=months, y=revenues, mode='lines+markers'))
    fig_line.update_layout(title='Revenue Over Time (Line Chart)',
                           xaxis_title='Month',
                           yaxis_title='Revenue')
    plot_div_line = plot(fig_line, output_type='div', include_plotlyjs=False)

    # Sample data for bar chart
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=months, y=revenues, marker_color='pink'))
    fig_bar.update_layout(title='Revenue Over Time (Bar Chart)',
                          xaxis_title='Month',
                          yaxis_title='Revenue')
    plot_div_bar = plot(fig_bar, output_type='div', include_plotlyjs=False)

    return render(request, 'magasin/plot_exm.html', {'plot_div_line': plot_div_line, 'plot_div_bar': plot_div_bar})
class ProduitAPIView(APIView):
    def get(self, request, *args, **kwargs):
        produits = Produit.objects.all()
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)
class CategoryAPIView(APIView):
 def get(self, *args, **kwargs):
  categories = Categorie.objects.all()
  serializer = CategorySerializer(categories, many=True)
  return Response(serializer.data)
class ProductViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProduitSerializer

    def get_queryset(self):
        queryset = Produit.objects.all()
        category_id = self.request.GET.get('category_id')
        
        if category_id:
            try:
                # Check if the category_id corresponds to an existing Categorie object
                categorie = Categorie.objects.get(id=category_id)
            except Categorie.DoesNotExist:

                # If the category does not exist, return an empty queryset
                return Produit.objects.none()
            
            # Filter the queryset by the specified category_id
            queryset = queryset.filter(categorie_id=category_id)
            
        return queryset
