from rest_framework import viewsets
from .models import Pet, Owner
from .serializers import PetSerializer, OwnerSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from vet_management.helpers import CookieJWTAuthentication

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'species', 'sex', 'owner__name']
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

 
class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]