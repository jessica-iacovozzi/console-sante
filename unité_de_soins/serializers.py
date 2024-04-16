from django.utils import formats
from django.utils.translation import activate
from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from .models import DossierMédical, Patient, PersonnelSoignant, RendezVous


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
    dernier_changement = serializers.SerializerMethodField()

    class Meta:
        model = DossierMédical
        fields = ['patient', 'incontinence', 'détection_chute', 'amnamèse_ic', 'fréquence_cardiaque', 'saturation', 'pression_artérielle', 'température_corporelle', 'fréquence_respiratoire', 'adhérence_rx', 'taille', 'poids', 'dernier_changement']

    def get_dernier_changement(self, obj):
        activate('fr')
        return formats.date_format(obj.dernier_changement, format='j F, H:i')

class PersonnelSoignantSerializer(serializers.ModelSerializer):
    patients = serializers.StringRelatedField(many=True)
    nombre_de_patients = serializers.IntegerField(read_only=True)

    class Meta:
        model = PersonnelSoignant
        fields = ['prénom', 'nom', 'role', 'département', 'nombre_de_patients', 'patients']

class RendezVousSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    personnel_soignant = serializers.StringRelatedField(many=True)
    date = serializers.SerializerMethodField()
    durée = serializers.SerializerMethodField()

    class Meta:
        model = RendezVous
        fields = ['description', 'lieu', 'date', 'durée', 'patient', 'personnel_soignant']

    def get_date(self, obj):
        activate('fr')
        return formats.date_format(obj.date, format='j F, Hh%i')

    def get_durée(self, obj):
        activate('fr')
        hours, minutes = divmod(obj.durée.seconds // 60, 60)
        formatted_duration = ""
        if hours:
            formatted_duration += f"{hours}h "
        if minutes:
            formatted_duration += f"{minutes}min"
        return formatted_duration.strip()
