from django.db.models.aggregates import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import DossierMédical, Patient, PersonnelSoignant, RendezVous
from .serializers import DossierMédicalSerializer, PatientSerializer, PersonnelSoignantSerializer, RendezVousSerializer

class DossierMédicalViewSet(ModelViewSet):
    queryset = DossierMédical.objects.select_related('patient').all()
    serializer_class = DossierMédicalSerializer

class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.prefetch_related('rendez_vous').select_related('adresse').all()
    serializer_class = PatientSerializer

class PersonnelSoignantViewSet(ModelViewSet):
    queryset = PersonnelSoignant.objects.prefetch_related('rendezvous_set', 'patients').annotate(
        nombre_de_patients=Count('patients')
    ).all()
    serializer_class = PersonnelSoignantSerializer

class RendezVousViewSet(ModelViewSet):
    serializer_class = RendezVousSerializer

    def get_queryset(self):
        return RendezVous.objects.filter(patient_id=self.kwargs['patient_pk'])

    def get_serializer_context(self):
        return {'patient_id': self.kwargs['patient_pk']}
