from rest_framework import status
import pytest
from model_bakery import baker
from unité_de_soins.models import Adresse, Patient


@pytest.fixture
def create_patient(api_client):
    def do_create_patient(patient):
        return api_client.post('/soins/patients/', patient)
    return do_create_patient

@pytest.mark.django_db
class TestCreatePatient:
    def test_if_user_is_anonymous_returns_401(self, create_patient):
        response = create_patient({'prénom': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_patient):
        authenticate()

        response = create_patient({'prénom': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_patient):
        authenticate(is_staff=True)

        response = create_patient({'prénom': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['prénom'] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_patient):
        authenticate(is_staff=True)
        adresse = baker.make(Adresse)

        response = create_patient({
            "prénom": "Jane",
            "nom": "Doe",
            "courriel": "janedoe@gmail.com",
            "adresse": adresse.id,
            "date_de_naissance": "1975-01-01",
            "ramq": "DOEJ12345678"
        })

        assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
class TestRetrievePatient:
    def test_if_user_is_anonymous_return_401(self, api_client):
        response = api_client.get('/soins/patients/101/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, authenticate, api_client):
        authenticate()

        response = api_client.get('/soins/patients/101/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_admin_but_patient_does_not_exist_return_404(self, authenticate, api_client):
        authenticate(is_staff=True)

        response = api_client.get('/soins/patients/101/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_admin_and_patient_exists_return_200(self, authenticate, api_client):
        authenticate(is_staff=True)
        patient = baker.make(Patient)

        response = api_client.get(f'/soins/patients/{patient.id}/')

        assert response.status_code == status.HTTP_200_OK
