from rest_framework import serializers
from .models import Patient, DossierMédical, PersonnelSoignant, RendezVous
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

class PatientSerializer(serializers.ModelSerializer):
    adresse = serializers.StringRelatedField()
    rendez_vous = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='patient-rendezvous-detail',
        parent_lookup_kwargs={'patient_pk': 'patient__pk'}
    )

    class Meta:
        model = Patient
        fields = ['prénom', 'nom', 'adresse', 'date_de_naissance', 'ramq', 'rendez_vous']

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
        fields = ['prénom', 'nom', 'role', 'département', 'nombre_de_patients', 'patients']

class RendezVousSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    personnel_soignant = serializers.StringRelatedField(many=True)

    class Meta:
        model = RendezVous
        fields = ['description', 'lieu', 'date', 'durée', 'patient', 'personnel_soignant']
