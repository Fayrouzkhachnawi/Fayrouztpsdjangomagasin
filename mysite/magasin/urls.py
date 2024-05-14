from django.urls import path, include
from . import views
from .views import ProduitAPIView
from .views import CategoryAPIView, ProductViewset
from rest_framework import routers
router = routers.SimpleRouter()
router.register('produit', ProductViewset, basename='produit')
urlpatterns = [ 
     path('magasin/mesProduits.html', views.index, name='index'),
     path('magasin/mesFournisseurs.html', views.fournisseur, name='fournisseur'),
     path('magasin/mesCommandes.html', views.commande, name='commande'),
     path('magasin/majProduits.html', views.indajout, name='indajout'),
     path('magasin/vitrine.html', views.vitrineindex, name='vitrineindex'),
     path('magasin/nouveauFournisseur.html', views.nouveauFournisseur, name='nouveauFournisseur'),
     path('magasin/majCommandes.html', views.nouveauCommande, name='nouveauCommande'),
     path('', views.home, name='home'),
     path('register/',views.register, name = 'register'),
      path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
       path('cart/', views.cart_view, name='cart'),
        path('update_quantity/<int:cart_item_id>/', views.update_quantity, name='update_quantity'),
         path('checkout/', views.checkout, name='checkout'),
          path('cart/delete/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),
            path('produit/<int:produit_id>/delete/', views.delete_produit, name='delete_produit'),
            path('fournisseur/<int:fournisseur_id>/delete/', views.delete_fournisseur, name='delete_fournisseur'),
             path('commande/<int:commande_id>/delete/', views.delete_commande, name='delete_commande'),
               path('commande/<int:commande_id>/update/', views.update_commande, name='update_commande'),
               path('fournisseur/<int:fournisseur_id>/update/', views.update_fournisseur, name='update_fournisseur'),
        path('produit/<int:produit_id>/update/', views.update_produit, name='update_produit'),
   
         path('contact/', views.contact, name='contact'),
         path('magasin/plot_exm.html', views.plot_exampletwo, name='plot_exampletwo'),
          path('api/produit/', ProduitAPIView.as_view()),
          path('api/category/', CategoryAPIView.as_view()),
           path('api/', include(router.urls)),

          

]

