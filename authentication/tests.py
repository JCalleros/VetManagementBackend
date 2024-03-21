from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser
import jwt
import os

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(email='testuser@test.com', first_name='Mario', last_name='Alberto', role='vet')
        self.user.set_password('ComplexPassword123!')
        self.user.save()


    def test_obtain_pair(self):
        response = self.client.post(reverse('token-obtain-pair'), {'email': 'testuser@test.com', 'password': 'ComplexPassword123!'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('refresh_token', response.cookies)
        self.assertIn('access_token', response.cookies)
        

    def test_obtain_pair_payload(self):
        response = self.client.post(reverse('token-obtain-pair'), {'email': 'testuser@test.com', 'password': 'ComplexPassword123!'})
        self.client.cookies['refresh_token'] = response.cookies['refresh_token']
        self.client.cookies['access_token'] = response.cookies['access_token']
        access_token = self.client.cookies['access_token'].value
        payload = jwt.decode(access_token, os.getenv('SECRET_KEY'), algorithms=settings.SIMPLE_JWT['ALGORITHM'])
        self.assertEqual(payload['user_id'], self.user.id)
        self.assertEqual(payload['email'], self.user.email)
        self.assertEqual(payload['role'], self.user.role)


    def test_refresh_token(self):
        response = self.client.post(reverse('token-obtain-pair'), {'email': 'testuser@test.com', 'password': 'ComplexPassword123!'})
        self.client.cookies['refresh_token'] = response.cookies['refresh_token']
        self.client.cookies['access_token'] = response.cookies['access_token']
        response = self.client.post(reverse('token-refresh'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data['access']
        payload = jwt.decode(access_token, os.getenv('SECRET_KEY'), algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
        self.assertEqual(payload['user_id'], self.user.id)
        self.assertEqual(payload['email'], self.user.email)
        self.assertEqual(payload['role'], self.user.role)

   
    def test_verify_token(self):
        response = self.client.post(reverse('token-obtain-pair'), {'email': 'testuser@test.com', 'password': 'ComplexPassword123!'})
        self.client.cookies['refresh_token'] = response.cookies['refresh_token']
        self.client.cookies['access_token'] = response.cookies['access_token']
        response = self.client.post(reverse('token-verify'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
