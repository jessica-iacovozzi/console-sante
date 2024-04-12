from django.urls import path
from django.urls.conf import include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('dossiers', views.DossierMédicalViewSet)
router.register('patients', views.PatientViewSet)
router.register('personnel', views.PersonnelSoignantViewSet)
router.register('rendezvous', views.RendezVousViewSet)

urlpatterns = router.urls
