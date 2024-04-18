from django.db.models import Q
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from .filters import PersonnelSoignantFilter
from .models import DossierMédical, Patient, PersonnelSoignant, RendezVous
from .serializers import (CreateRendezVousSerializer, DossierMédicalSerializer,
                          PatientSerializer, PersonnelSoignantSerializer,
                          RendezVousSerializer)


class DossierMédicalViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = DossierMédical.objects.select_related('patient').all()
    serializer_class = DossierMédicalSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['incontinence', 'détection_chute', 'amnamèse_ic', 'fréquence_cardiaque', 'saturation', 'pression_artérielle', 'température_corporelle', 'fréquence_respiratoire', 'adhérence_rx']
    ordering_fields = ['dernier_changement']

class PatientViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Patient.objects.prefetch_related('rendez_vous__personnel_soignant', 'rendez_vous__personnel_soignant__user').select_related('adresse').all()
    serializer_class = PatientSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nom', 'prénom', 'courriel', 'téléphone_maison', 'téléphone_cellulaire', 'ramq']
    ordering_fields = ['date_de_naissance']

class PersonnelSoignantViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = PersonnelSoignant.objects.prefetch_related('patients', 'rendez_vous__patient', 'rendez_vous__personnel_soignant', 'rendez_vous__personnel_soignant__user').select_related('user').annotate(
        nombre_de_patients=Count('patients')
    ).all()
    serializer_class = PersonnelSoignantSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PersonnelSoignantFilter
    search_fields = ['user__first_name', 'user__last_name', 'département']
    ordering_fields = ['nombre_de_patients']

class RendezVousViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = RendezVous.objects.prefetch_related('personnel_soignant', 'personnel_soignant__user').select_related('patient').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['date', 'durée']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateRendezVousSerializer
        return RendezVousSerializer

class PatientRendezVousViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = RendezVousSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    def get_queryset(self):
        return RendezVous.objects.prefetch_related('personnel_soignant', 'personnel_soignant__user').select_related('patient').filter(
            patient_id=self.kwargs['patient_pk']
        )

class PersonnelRendezVousViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = RendezVousSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['patient']

    def get_queryset(self):
        return RendezVous.objects.prefetch_related('personnel_soignant', 'personnel_soignant__user').select_related('patient').filter(
            personnel_soignant=self.kwargs['personnel_pk']
        )
