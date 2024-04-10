from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DossierMédical
from .serializers import DossierMédicalSerializer

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
def détails_patient(request, pk):
    return Response('ok')
