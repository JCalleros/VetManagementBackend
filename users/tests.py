from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core import mail
from rest_framework.test import APITestCase
from .models import CustomUser


class CustomUserTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='testuser@gmail.com', role='vet')
        self.user.set_password('ComplexPassword123!')
        self.user.save()

    def test_create_user(self):
        url = reverse('create-user')
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "newuser@gmail.com",
            "phone_number": "+526434318623",
            "password": "ComplexPassword123!",
            "password2": "ComplexPassword123!",
            "role": "vet"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(email='newuser@gmail.com').role, 'vet')

    def test_read_user(self):
        url = reverse('current-user')
        self.client.login(email='testuser@gmail.com', password='ComplexPassword123!')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'testuser@gmail.com')

    def test_update_user(self):
        url = reverse('current-user')
        data = {
            "role": "assistant"
        }
        self.client.login(email='testuser@gmail.com', password='ComplexPassword123!')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.get(email='testuser@gmail.com').role, 'assistant')

    def test_delete_user(self):
        url = reverse('current-user')
        self.client.login(email='testuser@gmail.com', password='ComplexPassword123!')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 0)
