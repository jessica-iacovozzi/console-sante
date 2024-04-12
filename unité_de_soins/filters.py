from django_filters.rest_framework import FilterSet
from .models import PersonnelSoignant

class PersonnelSoignantFilter(FilterSet):
    class Meta:
        model = PersonnelSoignant
        fields = {
            'prénom': ['exact'],
            'nom': ['exact'],
            'role': ['exact'],
            'département': ['exact', 'contains']
        }
