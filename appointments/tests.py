

from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient
from pets.models import Pet
from users.models import CustomUser
from .models import Appointment
import jwt


class AppointmentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.pet = Pet.objects.create(name='Fido', species='Dog', sex='M')
        self.user = CustomUser.objects.create(email='testuser@example.com', role='vet')
        self.appointment = Appointment.objects.create(pet=self.pet, date="2024-03-13T15:33:23Z")
        payload = {'email': 'testuser@example.com'}
        jwt_token = jwt.encode(payload, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm='HS256')
        self.client.cookies['access_token'] = jwt_token
        
    def test_create_appointment(self):
        url = reverse('appointment-list')
        data = {
            "pet": self.pet.id,
            "date": "2024-03-13T15:33:23Z",
            "details": "Regular checkup for vaccinations",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_all_appointments(self):
        url = reverse('appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_read_appointment(self):
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['date'], self.appointment.date)
        self.assertEqual(response.data['pet'], self.appointment.pet.pk)

    def test_update_appointment(self):
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.pk})
        data = {
            'pet': self.pet.id,
            'date': "2024-03-15T15:33:23Z",
            'details': 'Update testing'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['details'], 'Update testing')

    def test_partial_update_details_appointment(self):
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.pk})
        data = {
            'details': 'Changing details'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['details'], 'Changing details')

    def test_partial_update_dete_appointment(self):
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.pk})
        data = {
            'date': '2024-03-17T17:00:00Z'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['date'], '2024-03-17T17:00:00Z')

    def test_delete_appointment(self):
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
