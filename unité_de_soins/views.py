from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from .filters import PersonnelSoignantFilter
from .models import DossierMédical, Patient, PersonnelSoignant, RendezVous
from .serializers import (DossierMédicalSerializer, PatientSerializer,
                          PersonnelSoignantSerializer, RendezVousSerializer)


class DossierMédicalViewSet(ModelViewSet):
    queryset = DossierMédical.objects.select_related('patient').all()
    serializer_class = DossierMédicalSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['incontinence', 'détection_chute', 'amnamèse_ic', 'fréquence_cardiaque', 'saturation', 'pression_artérielle', 'température_corporelle', 'fréquence_respiratoire', 'adhérence_rx']
    ordering_fields = ['dernier_changement']

class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.prefetch_related('rendez_vous').select_related('adresse').all()
    serializer_class = PatientSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nom', 'prénom', 'courriel', 'téléphone_maison', 'téléphone_cellulaire', 'ramq']
    ordering_fields = ['date_de_naissance']

class PersonnelSoignantViewSet(ModelViewSet):
    queryset = PersonnelSoignant.objects.prefetch_related('patients').annotate(
        nombre_de_patients=Count('patients')
    ).all()
    serializer_class = PersonnelSoignantSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PersonnelSoignantFilter
    search_fields = ['nom', 'prénom', 'département']
    ordering_fields = ['nombre_de_patients']

class RendezVousViewSet(ModelViewSet):
    serializer_class = RendezVousSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['patient', 'personnel_soignant']
    ordering_fields = ['date', 'durée']

    def get_queryset(self):
        return RendezVous.objects.filter(patient_id=self.kwargs['patient_pk'])
