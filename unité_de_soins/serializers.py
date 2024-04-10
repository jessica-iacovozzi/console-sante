from rest_framework import serializers
from .models import Patient, DossierMédical, PersonnelSoignant

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['prénom', 'nom', 'adresse', 'date_de_naissance', 'ramq']

    adresse = serializers.StringRelatedField()

class DossierMédicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierMédical
        fields = ['patient', 'incontinence', 'détection_chute', 'amnamèse_ic', 'fréquence_cardiaque', 'saturation', 'pression_artérielle', 'température_corporelle', 'fréquence_respiratoire', 'adhérence_rx', 'taille', 'poids']

    patient = serializers.StringRelatedField()

class PersonnelSoignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonnelSoignant
        fields = ['prénom', 'nom', 'role', 'département']
