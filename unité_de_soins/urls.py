from django.urls import path
from . import views

urlpatterns = [
    path('dossiers/', views.dossiers_médicaux),
    path('dossiers/<int:pk>/', views.dossier_médical),
    path('patients/', views.patients),
    path('patients/<int:pk>/', views.patient),
    path('personnel/', views.liste_du_personnel),
    path('personnel/<int:pk>/', views.détail_personnel_soignant),
    path('rendezvous/', views.liste_de_rendez_vous),
    path('rendezvous/<int:pk>', views.détail_rendez_vous, name='rendezvous'),
]
