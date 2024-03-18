from django.db import models
from pets.models import Pet

class Appointment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    date = models.DateTimeField()
    # service = models.ForeignKey(Service, on_delete=models.SET_NULL)
    details = models.TextField(null=True, blank=True)
