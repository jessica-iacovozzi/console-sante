from django.contrib import admin
from . import models

@admin.register(models.Adresse)
class AdresseAdmin(admin.ModelAdmin):
    list_display = ['numéro_de_rue', 'rue', 'appartement', 'ville', 'code_postal', 'province']
    ordering = ['province', 'ville', 'code_postal']
    search_fields = ['rue__istartswith', 'ville__istartswith', 'code_postal__istartswith']

@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prénom', 'date_de_naissance', 'ramq']
    ordering = ['nom', 'prénom']
    search_fields = ['nom__istartswith', 'prénom__istartswith']
    autocomplete_fields = ['adresse']

@admin.register(models.DossierMédical)
class DossierMédicalAdmin(admin.ModelAdmin):
    list_display = ['id_dossier', 'chambre', 'incontinence', 'détection_chute', 'amnamèse_ic', 'fréquence_cardiaque', 'saturation', 'pression_artérielle', 'température_corporelle', 'fréquence_respiratoire', 'adhérence_rx', 'poids', 'taille', 'dernier_changement', 'patient']
    autocomplete_fields = ['patient']
    search_fields = ['id_dossier__istartswith']

@admin.register(models.PersonnelSoignant)
class PersonnelSoignant(admin.ModelAdmin):
    list_display = ['EIN', 'nom', 'prénom', 'role', 'département']
    ordering = ['nom', 'prénom']
