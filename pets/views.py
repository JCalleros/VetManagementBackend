from rest_framework import viewsets
from .models import Pet
from .serializers import PetSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'species', 'sex', 'owner__name']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]