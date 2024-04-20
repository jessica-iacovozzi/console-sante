from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import PersonnelSoignantFilter
from .models import DossierMédical, Patient, PersonnelSoignant, RendezVous
from .permissions import IsAdminOrReadOnly
from .serializers import (CreateDossierMédicalSerializer,
                          CreateOrUpdatePatientRendezVousSerializer,
                          CreateOrUpdatePatientSerializer,
                          CreateOrUpdatePersonnelRendezVousSerializer,
                          CreateOrUpdatePersonnelSoignantSerializer,
                          CreateOrUpdateRendezVousSerializer,
                          DossierMédicalSerializer, PatientSerializer,
                          PersonnelSoignantSerializer, RendezVousSerializer)


class DossierMédicalViewSet(ModelViewSet):
    queryset = DossierMédical.objects.select_related('patient').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['incontinence', 'détection_chute', 'amnamèse_ic', 'fréquence_cardiaque', 'saturation', 'pression_artérielle', 'température_corporelle', 'fréquence_respiratoire', 'adhérence_rx']
    ordering_fields = ['dernier_changement']
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateDossierMédicalSerializer
        return DossierMédicalSerializer

class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.prefetch_related('rendez_vous__personnel_soignant', 'rendez_vous__personnel_soignant__user').select_related('adresse').all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nom', 'prénom', 'courriel', 'téléphone_maison', 'téléphone_cellulaire', 'ramq']
    ordering_fields = ['date_de_naissance']
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
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
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return CreateOrUpdatePersonnelSoignantSerializer
        return PersonnelSoignantSerializer

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (personnel, created) = PersonnelSoignant.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = PersonnelSoignantSerializer(personnel)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CreateOrUpdatePersonnelSoignantSerializer(personnel, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class RendezVousViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = RendezVous.objects.prefetch_related('personnel_soignant', 'personnel_soignant__user').select_related('patient').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['date', 'durée']
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return CreateOrUpdateRendezVousSerializer
        return RendezVousSerializer

class PatientRendezVousViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return RendezVous.objects.prefetch_related('personnel_soignant', 'personnel_soignant__user').select_related('patient').filter(
            patient_id=self.kwargs['patient_pk']
        )

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return CreateOrUpdatePatientRendezVousSerializer
        return RendezVousSerializer

class PersonnelRendezVousViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['patient']
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return RendezVous.objects.prefetch_related('personnel_soignant', 'personnel_soignant__user').select_related('patient').filter(
            personnel_soignant=self.kwargs['personnel_pk']
        )

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return CreateOrUpdatePersonnelRendezVousSerializer
        return RendezVousSerializer
