from django.db.models.aggregates import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PersonnelSoignantFilter
from .models import DossierMédical, Patient, PersonnelSoignant, RendezVous
from .serializers import DossierMédicalSerializer, PatientSerializer, PersonnelSoignantSerializer, RendezVousSerializer

class DossierMédicalViewSet(ModelViewSet):
    queryset = DossierMédical.objects.select_related('patient').all()
    serializer_class = DossierMédicalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['incontinence', 'détection_chute', 'amnamèse_ic', 'fréquence_cardiaque', 'saturation', 'pression_artérielle', 'température_corporelle', 'fréquence_respiratoire', 'adhérence_rx']

class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.prefetch_related('rendez_vous').select_related('adresse').all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nom', 'prénom', 'courriel', 'téléphone_maison', 'téléphone_cellulaire', 'ramq']

class PersonnelSoignantViewSet(ModelViewSet):
    queryset = PersonnelSoignant.objects.prefetch_related('patients').annotate(
        nombre_de_patients=Count('patients')
    ).all()
    serializer_class = PersonnelSoignantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PersonnelSoignantFilter

class RendezVousViewSet(ModelViewSet):
    queryset = RendezVous.objects.prefetch_related('personnel_soignant').select_related('patient').all()
    serializer_class = RendezVousSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient', 'personnel_soignant']
