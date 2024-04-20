from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('dossiers', views.DossierMédicalViewSet, basename='dossiers')
router.register('patients', views.PatientViewSet, basename='patients')
router.register('personnel', views.PersonnelSoignantViewSet, basename='personnel')
router.register('rendezvous', views.RendezVousViewSet, basename='rendezvous')

patients_router = routers.NestedDefaultRouter(router, 'patients', lookup='patient')
patients_router.register('rendezvous', views.PatientRendezVousViewSet, basename='patient-rendezvous')

personnel_router = routers.NestedDefaultRouter(router, 'personnel', lookup='personnel')
personnel_router.register('rendezvous', views.PersonnelRendezVousViewSet, basename='personnel-rendezvous')
personnel_router.register('photos', views.PersonnelSoignantPhotosViewSet, basename='personnel-photos')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(patients_router.urls)),
    path('', include(personnel_router.urls)),
]
