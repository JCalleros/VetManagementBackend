from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet, OwnerViewSet

router = DefaultRouter()
router.register(r'', PetViewSet)
router.register(r'owners', OwnerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]