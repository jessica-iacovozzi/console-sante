from django.db.models import Q
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from .filters import PersonnelSoignantFilter
from .models import DossierMédical, Patient, PersonnelSoignant, RendezVous
from .serializers import (CreateOrUpdatePatientRendezVousSerializer, CreateOrUpdatePatientSerializer, CreateOrUpdatePersonnelRendezVousSerializer,
                          CreateOrUpdateRendezVousSerializer, DossierMédicalSerializer,
                          PatientSerializer, PersonnelSoignantSerializer,
                          RendezVousSerializer, CreateOrUpdatePersonnelSoignantSerializer)


class DossierMédicalViewSet(ModelViewSet):
    queryset = DossierMédical.objects.select_related('patient').all()
    serializer_class = DossierMédicalSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['incontinence', 'détection_chute', 'amnamèse_ic', 'fréquence_cardiaque', 'saturation', 'pression_artérielle', 'température_corporelle', 'fréquence_respiratoire', 'adhérence_rx']
    ordering_fields = ['dernier_changement']

class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.prefetch_related('rendez_vous__personnel_soignant', 'rendez_vous__personnel_soignant__user').select_related('adresse').all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nom', 'prénom', 'courriel', 'téléphone_maison', 'téléphone_cellulaire', 'ramq']
    ordering_fields = ['date_de_naissance']

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return CreateOrUpdatePatientSerializer
        return PatientSerializer

class PersonnelSoignantViewSet(ModelViewSet):
    queryset = PersonnelSoignant.objects.prefetch_related('patients', 'rendez_vous__patient', 'rendez_vous__personnel_soignant', 'rendez_vous__personnel_soignant__user').select_related('user').annotate(
        nombre_de_patients=Count('patients')
    ).all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PersonnelSoignantFilter
    search_fields = ['user__first_name', 'user__last_name', 'département']
    ordering_fields = ['nombre_de_patients']

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return CreateOrUpdatePersonnelSoignantSerializer
        return PersonnelSoignantSerializer

class RendezVousViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = RendezVous.objects.prefetch_related('personnel_soignant', 'personnel_soignant__user').select_related('patient').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['date', 'durée']

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return CreateOrUpdateRendezVousSerializer
        return RendezVousSerializer

class PatientRendezVousViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    def get_queryset(self):
        return RendezVous.objects.prefetch_related('personnel_soignant', 'personnel_soignant__user').select_related('patient').filter(
            patient_id=self.kwargs['patient_pk']
        )

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return CreateOrUpdatePatientRendezVousSerializer
        return RendezVousSerializer

class PersonnelRendezVousViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['patient']

    def get_queryset(self):
        return RendezVous.objects.prefetch_related('personnel_soignant', 'personnel_soignant__user').select_related('patient').filter(
            personnel_soignant=self.kwargs['personnel_pk']
        )

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return CreateOrUpdatePersonnelRendezVousSerializer
        return RendezVousSerializer
