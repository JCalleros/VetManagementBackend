from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Pet, Owner
from users.models import CustomUser
import jwt 

class PetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = Owner.objects.create(full_name='John Doe', phone_number='+526434318623', contact='johndoe@example.com', address='123 Main St')
        self.pet = Pet.objects.create(name='Fido', species='Dog', breed='Mix', sex='M', age_years=1)
        self.pet.owners.add(self.owner)
        self.user = CustomUser.objects.create(email='testuser@example.com', role='vet')
        self.user.set_password('ComplexPassword123!')
        self.user.save()
        payload = {'email': 'testuser@example.com'}
        jwt_token = jwt.encode(payload, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm='HS256')
        self.client.cookies['access_token'] = jwt_token
        
    def test_create_pet(self):
        url = reverse('pet-list')
        data = {
            'name': 'Rex',
            'species': 'Dog',
            'sex': 'M',
            'breed': 'Mix',
            'age_years': 2,
            'owners': [self.owner.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Pet.objects.get(name='Rex').species, 'Dog')
        self.assertEqual(Pet.objects.get(name='Rex').age_years, 2)
        self.assertTrue(Pet.objects.get(id=response.data['id']).owners.filter(id=self.owner.id).exists())


    def test_create_pet_with_months_and_weeks(self):
        url = reverse('pet-list')
        data = {
            'name': 'Bella',
            'species': 'Cat',
            'breed': '',
            'sex': 'F',
            'age_years': 0,
            'age_months': 6,
            'age_weeks': 26,
            'owners': [self.owner.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Pet.objects.get(name='Bella').species, 'Cat')
        self.assertEqual(Pet.objects.get(name='Bella').age_years, 0)
        self.assertEqual(Pet.objects.get(name='Bella').age_months, 6)
        self.assertEqual(Pet.objects.get(name='Bella').age_weeks, 26)
        self.assertTrue(Pet.objects.get(id=response.data['id']).owners.filter(id=self.owner.id).exists())


    def test_create_pet_without_owner(self):
        url = reverse('pet-list')
        data = {
            'name': 'Stray',
            'species': 'Dog',
            'sex': 'M',
            'age_years': 1,
            'age_months': 12,
            'age_weeks': 52,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertFalse(Pet.objects.get(name='Stray').owners.exists())


    def test_create_duplicate_pet_without_owner(self):
        url = reverse('pet-list')
        data = {
            'name': 'Stray',
            'species': 'Dog',
            'sex': 'M',
            'age_years': 1,
            'age_months': 12,
            'age_weeks': 52,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
    
    def test_read_pet(self):
        url = reverse('pet-detail', kwargs={'pk': self.pet.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.pet.name)
        self.assertTrue(self.owner.id in response.data['owners'])
        
        
    def test_update_pet(self):
        url = reverse('pet-detail', kwargs={'pk': self.pet.pk})
        owner = Owner.objects.create(full_name='Omar', phone_number='+555434216892', contact='omar@example.com')
    
        data = {
            'name': 'Fido',
            'species': 'Dog',
            'sex': 'M',
            'owners': [owner.id]
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.pet.refresh_from_db()
        self.assertEqual(self.pet.name, 'Fido')
        self.assertEqual(self.pet.species, 'Dog')
        self.assertEqual(self.pet.sex, 'M')
        self.assertEqual(list(self.pet.owners.all()), [owner])
        

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
        owner = Owner.objects.create(full_name='Juan Mendez', phone_number='+578434213256', contact='juanm@example.com')
        current_owners = list(self.pet.owners.values_list('id', flat=True))
        current_owners.append(owner.id)
        data = {
            "owners": current_owners,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.pet.refresh_from_db()
        self.assertTrue(owner.id in list(self.pet.owners.values_list('id', flat=True)))
        self.assertTrue(self.pet.owners, current_owners)
        
        
    def test_delete_pet(self):
        url = reverse('pet-detail', kwargs={'pk': self.pet.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Pet.objects.count(), 0)


class OwnerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = Owner.objects.create(full_name='John Doe', phone_number='+526434318623', contact='johndoe@example.com', address='123 Main St')
        self.user = CustomUser.objects.create(email='testuser@example.com', role='vet')
        payload = {'email': 'testuser@example.com'}
        jwt_token = jwt.encode(payload, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm='HS256')
        self.client.cookies['access_token'] = jwt_token

    def test_create_owner(self):
        url = reverse('owner-list')
        data = {
            'full_name': 'Jane Doe',
            'phone_number': '+526434318620',
            'contact': 'janedoe@example.com',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Owner.objects.get(full_name='Jane Doe').contact, 'janedoe@example.com')
        self.assertEqual(Owner.objects.get(full_name='Jane Doe').phone_number, '+526434318620')
    
    def test_get_owner(self):
        url = reverse('owner-detail', kwargs={'pk': self.owner.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['full_name'], self.owner.full_name)
        self.assertEqual(response.data['phone_number'], self.owner.phone_number)
            
    def test_update_owner(self):
        url = reverse('owner-detail', kwargs={'pk': self.owner.pk})
        data = {
            'full_name': 'Jane Doe Changed',
            'phone_number': '+526434318621',
            'contact': 'janedoe@example.com',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.contact, 'janedoe@example.com')
 
    def test_partial_update_owner(self):
        url = reverse('owner-detail', kwargs={'pk': self.owner.pk})
        data = {
            'full_name': 'Jane Doe RE-Changed',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.full_name, 'Jane Doe RE-Changed')
           
    def test_delete_owner(self):
        url = reverse('owner-detail', kwargs={'pk': self.owner.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Owner.objects.count(), 0)