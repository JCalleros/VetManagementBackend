from rest_framework import serializers, viewsets
from .models import Pet, Owner

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id', 'name', 'contact', 'address']

class PetSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(allow_null=True)

    class Meta:
        model = Pet
        fields = ['name', 'species', 'sex', 'breed', 'age_years', 'age_months', 'age_weeks', 'color', 'owner']

    def create(self, validated_data):
        owner_data = validated_data.pop('owner', None)
        owner = Owner.objects.create(**owner_data) if owner_data else None
        pet = Pet.objects.create(owner=owner, **validated_data)
        return pet
    
    def update(self, instance, validated_data):
        owner_data = validated_data.pop('owner', None)
        if owner_data is not None:
            owner = instance.owner
            if owner is not None:
                for attr, value in owner_data.items():
                    setattr(owner, attr, value)
                owner.save()
            else:
                owner = Owner.objects.create(**owner_data)
                instance.owner = owner
        return super().update(instance, validated_data)