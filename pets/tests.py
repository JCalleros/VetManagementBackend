from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Pet, Owner
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class PetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = Owner.objects.create(name='John Doe', contact='johndoe@example.com', address='123 Main St')
        self.pet = Pet.objects.create(name='Fido', species='Dog', sex='M', owner=self.owner, age_years=1)
        self.user = CustomUser.objects.create(email='testuser@gmail.com', role='vet')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_pet(self):
        url = reverse('pet-list')
        data = {
            'name': 'Rex',
            'species': 'Dog',
            'sex': 'M',
            'age_years': 2,
            'owner': {
                'name': 'Jane Doe',
                'contact': 'janedoe@example.com',
                'address': '456 Main St'
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Pet.objects.get(name='Rex').species, 'Dog')
        self.assertEqual(Pet.objects.get(name='Rex').age_years, 2)


    def test_create_pet_with_months_and_weeks(self):
        url = reverse('pet-list')
        data = {
            'name': 'Bella',
            'species': 'Cat',
            'sex': 'F',
            'age_years': 0,
            'age_months': 6,
            'age_weeks': 26,
            'owner': {
                'name': 'John Doe',
                'contact': 'johndoe@example.com',
                'address': '123 Main St'
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Pet.objects.get(name='Bella').species, 'Cat')
        self.assertEqual(Pet.objects.get(name='Bella').age_years, 0)
        self.assertEqual(Pet.objects.get(name='Bella').age_months, 6)
        self.assertEqual(Pet.objects.get(name='Bella').age_weeks, 26)


    def test_create_pet_without_owner(self):
        url = reverse('pet-list')
        data = {
            'name': 'Stray',
            'species': 'Dog',
            'sex': 'M',
            'age_years': 1,
            'age_months': 12,
            'age_weeks': 52,
            'owner': None
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Pet.objects.get(name='Stray').owner, None)
    
    
    def test_read_pet(self):
        url = reverse('pet-detail', kwargs={'pk': self.pet.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.pet.name)


    def test_update_pet(self):
        url = reverse('pet-detail', kwargs={'pk': self.pet.pk})
        
        data = {
            'name': 'Fido',
            'species': 'Dog',
            'sex': 'M',
            'owner': {
                'name': 'Jane Doe',
                'contact': 'janedoe@example.com',
                'address': '456 Main St'
            }
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.owner.name, 'Jane Doe')


    def test_partial_update_pet(self):
        url = reverse('pet-detail', kwargs={'pk': self.pet.pk})
        data = {
            'name': 'Buddy',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.name, 'Buddy')

    def test_partial_update_owner(self):
        url = reverse('pet-detail', kwargs={'pk': self.pet.pk})
        data = {
            'owner': {
                'name': 'Jane Doe',
            }
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.owner.name, 'Jane Doe')
    
    
    def test_delete_pet(self):
        url = reverse('pet-detail', kwargs={'pk': self.pet.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Pet.objects.count(), 0)


class OwnerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = Owner.objects.create(name='John Doe', contact='johndoe@example.com', address='123 Main St')
        self.user = CustomUser.objects.create(email='testuser@gmail.com', role='vet')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_owner(self):
        url = reverse('owner-list')
        data = {
            'name': 'Jane Doe',
            'contact': 'janedoe@example.com',
            'address': '456 Main St'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Owner.objects.get(name='Jane Doe').contact, 'janedoe@example.com')
        self.assertEqual(Owner.objects.get(name='Jane Doe').address, '456 Main St')
    
    def test_get_owner(self):
        url = reverse('owner-detail', kwargs={'pk': self.owner.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.owner.name)
            
    def test_update_owner(self):
        url = reverse('owner-detail', kwargs={'pk': self.owner.pk})
        data = {
            'name': 'Jane Doe Changed',
            'contact': 'janedoe@example.com',
            'address': '454 Main St'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.contact, 'janedoe@example.com')
        self.assertEqual(self.owner.address, '454 Main St')
 
    def test_partial_update_owner(self):
        url = reverse('owner-detail', kwargs={'pk': self.owner.pk})
        data = {
            'name': 'Jane Doe RE-Changed',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.name, 'Jane Doe RE-Changed')
        
    
    def test_delete_owner(self):
        url = reverse('owner-detail', kwargs={'pk': self.owner.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Owner.objects.count(), 0)