from django.utils import formats
from django.utils.translation import activate
from rest_framework import serializers

from .models import DossierMédical, Patient, PersonnelSoignant, RendezVous


class SimplePatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['prénom', 'nom', 'ramq']

class SimplePersonnelSoignantSerializer(serializers.ModelSerializer):
    fonction = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = PersonnelSoignant
        fields = ['prénom', 'nom', 'fonction']

class RendezVousSerializer(serializers.ModelSerializer):
    patient = SimplePatientSerializer()
    personnel_soignant = SimplePersonnelSoignantSerializer(many=True)
    date = serializers.SerializerMethodField()
    durée = serializers.SerializerMethodField()

    class Meta:
        model = RendezVous
        fields = ['id', 'description', 'lieu', 'date', 'durée', 'patient', 'personnel_soignant']

    def get_date(self, obj):
        activate('fr')
        return formats.date_format(obj.date, format='j F, H:i')

    def get_durée(self, obj):
        hours, minutes = divmod(obj.durée.seconds // 60, 60)
        formatted_duration = ""
        if hours:
            formatted_duration += f"{hours}h "
        if minutes:
            formatted_duration += f"{minutes}min"
        return formatted_duration.strip()

class CreateOrUpdateRendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model = RendezVous
        fields = ['description', 'lieu', 'date', 'durée', 'patient', 'personnel_soignant']

class CreateOrUpdatePatientRendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model = RendezVous
        fields = ['description', 'lieu', 'date', 'durée', 'personnel_soignant']

class CreateOrUpdatePersonnelRendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model = RendezVous
        fields = ['description', 'lieu', 'date', 'durée', 'patient']

class PatientSerializer(serializers.ModelSerializer):
    adresse = serializers.StringRelatedField()
    rendez_vous = RendezVousSerializer(many=True)

    class Meta:
        model = Patient
        fields = ['id', 'prénom', 'nom', 'adresse', 'courriel', 'téléphone_maison', 'téléphone_cellulaire', 'télécopieur', 'date_de_naissance', 'ramq', 'rendez_vous']

class CreateOrUpdatePatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['prénom', 'nom', 'adresse', 'courriel', 'téléphone_maison', 'téléphone_cellulaire', 'télécopieur', 'date_de_naissance', 'ramq']

class DossierMédicalSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    dernier_changement = serializers.SerializerMethodField()

    class Meta:
        model = DossierMédical
        fields = ['id', 'patient', 'incontinence', 'détection_chute', 'amnamèse_ic', 'fréquence_cardiaque', 'saturation', 'pression_artérielle', 'température_corporelle', 'fréquence_respiratoire', 'adhérence_rx', 'taille', 'poids', 'dernier_changement']

    def get_dernier_changement(self, obj):
        activate('fr')
        return formats.date_format(obj.dernier_changement, format='j F, H:i')

class PersonnelSoignantSerializer(serializers.ModelSerializer):
    patients = serializers.StringRelatedField(many=True)
    nombre_de_patients = serializers.IntegerField(read_only=True)
    rendez_vous = RendezVousSerializer(many=True)

    class Meta:
        model = PersonnelSoignant
        fields = ['id', 'EIN', 'prénom', 'nom', 'role', 'département', 'courriel', 'nombre_de_patients', 'patients', 'rendez_vous']

class CreateOrUpdatePersonnelSoignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonnelSoignant
        fields = ['EIN', 'prénom', 'nom', 'role', 'département', 'courriel', 'patients']
