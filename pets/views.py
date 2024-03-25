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

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        species = request.data.get('species')
        sex = request.data.get('sex')
        owners = request.data.get('owners')
        if owners is not None:
            if Pet.objects.filter(name=name, species=species, sex=sex, owners__in=owners).exists():
                return Response({"detail": "A pet with these details already exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if Pet.objects.filter(name=name, species=species, sex=sex, owners__isnull=True).exists():
                return Response({"detail": "A pet with these details already exists."}, status=status.HTTP_400_BAD_REQUEST)
                
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        name = request.data.get('name')
        species = request.data.get('species')
        sex = request.data.get('sex')
        owners = request.data.get('owners')
        if owners is not None:
            if Pet.objects.filter(name=name, species=species, sex=sex, owners__in=owners).exclude(id=kwargs['pk']).exists():
                return Response({"detail": "A pet with these details already exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if Pet.objects.filter(name=name, species=species, sex=sex, owners__isnull=True).exclude(id=kwargs['pk']).exists():
                return Response({"detail": "A pet with these details already exists."}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    
    
class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['full_name', 'phone_number']
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]