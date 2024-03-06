from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from users.models import CustomUser

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(email='testuser@test.com', first_name='Mario', last_name='Alberto', role='vet')
        self.user.set_password('ComplexPassword123!')
        self.user.save()


    def test_obtain_pair(self):
        response = self.client.post(reverse('token_obtain_pair'), {'email': 'testuser@test.com', 'password': 'ComplexPassword123!'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)
        

    def test_obtain_pair_payload(self):
        response = self.client.post(reverse('token_obtain_pair'), {'email': 'testuser@test.com', 'password': 'ComplexPassword123!'})
        access_token = response.data['access']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        decoded_payload = AccessToken(access_token).payload
        self.assertEqual(decoded_payload['user_id'], self.user.id)
        self.assertEqual(decoded_payload['role'], self.user.role)
        self.assertEqual(decoded_payload['full_name'], f"{self.user.first_name} {self.user.last_name}")
        

    def test_refresh_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {'email': 'testuser@test.com', 'password': 'ComplexPassword123!'})
        refresh_token = response.data['refresh']
        response = self.client.post(reverse('token_refresh'), {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)


    def test_verify_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {'email': 'testuser@test.com', 'password': 'ComplexPassword123!'})
        access_token = response.data['access']
        response = self.client.post(reverse('token_verify'), {'token': access_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
