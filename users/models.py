from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('vet', 'Vet'),
        ('assistant', 'Assistant'),
    )
    
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default='vet')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

    
    def __str__(self):
        return self.email
    