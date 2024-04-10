from django.urls import path
from . import views

urlpatterns = [
    path('dossiers/', views.dossiers_médicaux),
    path('dossier/<int:id>/', views.dossier_médical),
    path('patients/<int:pk>/', views.détails_patient, name='détails_patient')
]
