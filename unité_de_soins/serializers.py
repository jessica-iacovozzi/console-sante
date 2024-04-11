from rest_framework import serializers
from .models import Patient, DossierMédical, PersonnelSoignant

class PatientSerializer(serializers.ModelSerializer):
    adresse = serializers.StringRelatedField()

    class Meta:
        model = Patient
        fields = ['prénom', 'nom', 'adresse', 'date_de_naissance', 'ramq']

class DossierMédicalSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()

    class Meta:
        model = DossierMédical
        fields = ['patient', 'incontinence', 'détection_chute', 'amnamèse_ic', 'fréquence_cardiaque', 'saturation', 'pression_artérielle', 'température_corporelle', 'fréquence_respiratoire', 'adhérence_rx', 'taille', 'poids']

class PersonnelSoignantSerializer(serializers.ModelSerializer):
    patients = serializers.StringRelatedField(many=True)
    nombre_de_patients = serializers.IntegerField(read_only=True)

    class Meta:
        model = PersonnelSoignant
        fields = ['prénom', 'nom', 'role', 'département', 'patients', 'nombre_de_patients']
