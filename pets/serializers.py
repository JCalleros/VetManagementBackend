from rest_framework import serializers, viewsets
from .models import Pet, Owner

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id', 'full_name', 'phone_number', 'contact', 'address')

class PetSerializer(serializers.ModelSerializer):
    owners = serializers.PrimaryKeyRelatedField(many=True, queryset=Owner.objects.all(), required=False)

    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'sex', 'breed', 'photo', 'age_years', 'age_months', 'age_weeks', 'color', 'owners']
