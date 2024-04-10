from rest_framework import serializers
from .models import Patient, DossierMédical

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'prénom', 'nom']

class DossierMédicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierMédical
        fields = ['id', 'patient', 'incontinence', 'détection_chute', 'amnamèse_ic', 'fréquence_cardiaque', 'saturation', 'pression_artérielle', 'température_corporelle', 'fréquence_respiratoire', 'adhérence_rx']
