from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import CustomUser

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(first_name="Jorge", last_name="Calleros", 
                                                email="ing.kyros.test@gmail.com",
                                                phone_number='+526644567637', role='vet')

      
    def test_create_user(self):
        url = reverse('user-list')
        data = {
            "first_name": "Luis",
            "last_name": "Martinez",
            "email": "prueba123@gmail.com",
            "phone_number": "+526434318623",
            "role": "vet"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CustomUser.objects.get(first_name='Luis').last_name, 'Martinez')
        self.assertEqual(CustomUser.objects.get(first_name='Luis').email, 'prueba123@gmail.com')
        self.assertEqual(CustomUser.objects.get(first_name='Luis').phone_number, '+526434318623')
        self.assertEqual(CustomUser.objects.get(first_name='Luis').role, 'vet')

      
    def test_read_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'ing.kyros.test@gmail.com')


    def test_update_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        
        data = {
            "first_name": "Maria",
            "last_name": "Juarez",
            "email": "prueba121@gmail.com",
            "phone_number": "+526434318642",
            "role": "vet"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Maria')
        self.assertEqual(self.user.last_name, 'Juarez')
        self.assertEqual(self.user.email, 'prueba121@gmail.com')
        self.assertEqual(self.user.phone_number, '+526434318642')

       
    def test_partial_update_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        data = {
            'role': 'assistant',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, 'assistant')


    def test_delete_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(CustomUser.objects.count(), 0)