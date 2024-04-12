from django.urls import path
from django.urls.conf import include
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('dossiers', views.DossierMédicalViewSet, basename='dossiers')
router.register('patients', views.PatientViewSet, basename='patients')
router.register('personnel', views.PersonnelSoignantViewSet, basename='personnel')

patients_router = routers.NestedDefaultRouter(router, 'patients', lookup='patient')
patients_router.register('rendezvous', views.RendezVousViewSet, basename='patient-rendezvous')

urlpatterns = router.urls + patients_router.urls
