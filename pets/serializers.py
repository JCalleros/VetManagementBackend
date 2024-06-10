from rest_framework import serializers, viewsets
from .models import Pet, Owner
from django.db.models import Q

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id', 'full_name', 'phone_number', 'email')

class PetSerializer(serializers.ModelSerializer):
    owners = serializers.PrimaryKeyRelatedField(many=True, queryset=Owner.objects.all(), required=False)

    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'sex', 'breed', 'photo', 'age_years', 'age_months', 'age_weeks', 'color', 'owners']

    def validate(self, data):
        name = data.get('name')
        species = data.get('species')
        sex = data.get('sex')
        owners = data.get('owners', None)
        
        filter_params = {
            'name': name,
            'species': species,
            'sex': sex,
        }

        if owners:
            filter_params['owners__in'] = owners
        else:
            filter_params['owners__isnull'] = True

        if Pet.objects.filter(**filter_params).exists():
            raise serializers.ValidationError("A pet with these details already exists.")

        return data