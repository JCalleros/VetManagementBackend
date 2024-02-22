from django.db import models

class Owner(models.Model):
    name = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)


class Pet(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    breed = models.CharField(max_length=150, blank=True)
    age_years = models.PositiveIntegerField(null=True, blank=True)
    age_months = models.PositiveIntegerField(null=True, blank=True)
    age_weeks = models.PositiveIntegerField(null=True, blank=True)
    color = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
