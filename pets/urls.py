from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet, OwnerViewSet

router = DefaultRouter()
router.register(r'pets', PetViewSet)
router.register(r'owners', OwnerViewSet)

urlpatterns = [
    path('v1/', include(router.urls))
]