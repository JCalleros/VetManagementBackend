from django.db import models
from django.core.validators import RegexValidator

class Owner(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    full_name = models.CharField(max_length=100, db_index=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Pet(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    breed = models.CharField(max_length=150, null=True, blank=True)
    age_years = models.PositiveIntegerField(null=True, blank=True)
    age_months = models.PositiveIntegerField(null=True, blank=True)
    age_weeks = models.PositiveIntegerField(null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='pet_images/', null=True, blank=True)
    owners = models.ManyToManyField(Owner, blank=True)
    

