from django.db import models
from django.conf import settings

from django.contrib import admin


class Adresse(models.Model):
    PROVINCE_CHOIX = {
        "NL": "Terre-Neuve-et-Labrador",
        "PE": "Île-du-Prince-Édouard",
        "NS": "Nouvelle-Écosse",
        "NB": "Nouveau-Brunswick",
        "QC": "Québec",
        "ON": "Ontario",
        "MB": "Manitoba",
        "SK": "Saskatchewan",
        "AB": "Alberta",
        "BC": "Colombie-Britannique",
        "YT": "Yukon",
        "NT": "Territoires du Nord-Ouest",
        "NU": "Nunavut"
    }

    numéro_de_rue = models.PositiveIntegerField()
    rue = models.CharField(max_length=255)
    appartement = models.PositiveSmallIntegerField(null=True, blank=True)
    ville = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=6)
    province = models.CharField(max_length=2, choices=PROVINCE_CHOIX)

    def __str__(self):
        return f'{self.numéro_de_rue} {self.rue}, {self.ville}, {self.code_postal}, {self.province}'

    class Meta:
        ordering = ['rue', 'numéro_de_rue']

class Patient(models.Model):
    nom = models.CharField(max_length=60)
    prénom = models.CharField(max_length=60)
    adresse = models.ForeignKey(Adresse, on_delete=models.PROTECT)
    courriel = models.EmailField(max_length=254, unique=True)
    téléphone_maison = models.CharField(max_length=12, null=True, blank=True)
    téléphone_cellulaire = models.CharField(max_length=12, null=True, blank=True)
    télécopieur = models.CharField(max_length=12, null=True, blank=True)
    date_de_naissance = models.DateField(auto_now=False)
    ramq = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return f'{self.prénom} {self.nom}'

    class Meta:
        ordering = ['nom', 'prénom']

class DossierMédical(models.Model):
    INCONTINENCE_CHOIX = [
        ('sèche', 'Sèche'),
        ('humide', 'Humide'),
        ('<1/2 plein', '<½ plein'),
        ('>1/2 plein', '>½ plein'),
        ('changer', 'Changer'),
    ]

    STATUT = [
        ('normal', 'Normal'),
        ('avertissement', 'Avertissement'),
        ('alerte', 'Alerte'),
        ('pas de données', 'Pas de données'),
        ('pas de suivi', 'Pas de suivi'),
    ]

    id_dossier = models.CharField(max_length=24, unique=True)
    chambre = models.CharField(max_length=5)
    incontinence = models.CharField(max_length=11, choices=INCONTINENCE_CHOIX)
    détection_chute = models.CharField(max_length=14, choices=STATUT)
    amnamèse_ic = models.CharField(max_length=14, choices=STATUT)
    fréquence_cardiaque = models.CharField(max_length=14, choices=STATUT)
    saturation = models.CharField(max_length=14, choices=STATUT)
    pression_artérielle = models.CharField(max_length=14, choices=STATUT)
    température_corporelle = models.CharField(max_length=14, choices=STATUT)
    fréquence_respiratoire = models.CharField(max_length=14, choices=STATUT)
    adhérence_rx = models.CharField(max_length=14, choices=STATUT)
    taille = models.DecimalField(max_digits=5, decimal_places=2)
    poids = models.DecimalField(max_digits=5, decimal_places=2)
    date_créé = models.DateTimeField(auto_now_add=True)
    dernier_changement = models.DateTimeField(auto_now=True)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.id_dossier

    class Meta:
        ordering = ['id_dossier']
        verbose_name_plural = "Dossier médicaux"

class PersonnelSoignant(models.Model):
    ROLES = {
        "DT": "Diététiste",
        "DR": "Docteur",
        "ERG": "Ergothérapeute",
        "INF": "Infirmier/Infirmière",
        "INFA": "Infirmier auxiliaire/Infirmière auxiliaire",
        "INH": "Inhalothérapeute",
        "OPT": "Optométriste",
        "ORT": "Orthophoniste",
        "PHA": "Pharmacien",
        "PHY": "Physiothérapeute",
        "POD": "Podiatre",
        "PSY": "Psychologue"
    }

    EIN = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=4, choices=ROLES)
    département = models.CharField(max_length=255)
    patients = models.ManyToManyField(Patient)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def prénom(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def nom(self):
        return self.user.last_name

    def courriel(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "Personnel soignant"

class PersonnelSoignantPhoto(models.Model):
    personnel_soignant = models.ForeignKey(PersonnelSoignant, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='unité_de_soins/photos')

class RendezVous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rendez_vous')
    personnel_soignant = models.ManyToManyField(PersonnelSoignant, related_name='rendez_vous')
    description = models.TextField(blank=True, null=True)
    lieu = models.CharField(max_length=255)
    date = models.DateTimeField()
    durée = models.DurationField()

    class Meta:
        ordering = ['date', 'durée']
        verbose_name = 'Rendez-vous'
        verbose_name_plural = 'Rendez-vous'
