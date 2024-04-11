from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DossierMédical, Patient, PersonnelSoignant, RendezVous
from .serializers import DossierMédicalSerializer, PatientSerializer, PersonnelSoignantSerializer, RendezVousSerializer

@api_view()
def dossiers_médicaux(request):
    queryset = DossierMédical.objects.select_related('patient').all()
    serializer = DossierMédicalSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@api_view()
def dossier_médical(request, id):
    dossier = get_object_or_404(DossierMédical, pk=id)
    serializer = DossierMédicalSerializer(dossier, context={'request': request})
    return Response(serializer.data)

@api_view()
def patients(request):
    queryset = Patient.objects.select_related('adresse').all()
    seriallizer = PatientSerializer(queryset, many=True, context={'request': request})
    return Response(seriallizer.data)

@api_view()
def patient(request, id):
    patient = get_object_or_404(Patient, pk=id)
    serializer = PatientSerializer(patient, context={'request': request})
    return Response(serializer.data)

@api_view()
def liste_du_personnel(request):
    queryset = PersonnelSoignant.objects.prefetch_related('patients').annotate(
        nombre_de_patients=Count('patients')
    ).all()
    serializer = PersonnelSoignantSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@api_view()
def détail_personnel_soignant(request, id):
    soigant = get_object_or_404(PersonnelSoignant, pk=id)
    serializer = PersonnelSoignantSerializer(soigant, context={'request': request})
    return Response(serializer.data)

@api_view()
def liste_de_rendez_vous(request):
    queryset = RendezVous.objects.prefetch_related('personnel_soignant').select_related('patient').all()
    serializer = RendezVousSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@api_view()
def détail_rendez_vous(request, id):
    rendezvous = get_object_or_404(RendezVous, pk=id)
    serializer = RendezVousSerializer(rendezvous, context={'request': request})
    return Response(serializer.data)
