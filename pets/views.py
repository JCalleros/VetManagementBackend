from rest_framework import viewsets
from .models import Pet, Owner
from .serializers import PetSerializer, OwnerSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from vet_management.helpers import CookieJWTAuthentication


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'species', 'sex', 'owners__full_name', 'owners__phone_number']
    ordering_fields = ['name', 'species']
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, re1quest, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page is not None else queryset, many=True)
        data = serializer.data
        
        for pet in data:
            owners_data = []
            for owner_id in pet['owners']:
                try:
                    owner = Owner.objects.get(id=owner_id)
                except Owner.DoesNotExist:
                    continue
                owner_data = {
                    'id': owner.id,
                    'full_name': owner.full_name,
                    'phone_number': owner.phone_number,
                    'email': owner.email,
                }
                owners_data.append(owner_data)
            pet['owners'] = owners_data

        return self.get_paginated_response(data) if page is not None else Response(data)

        
    
    
class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['full_name', 'phone_number']
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]