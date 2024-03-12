from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet
router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet) 

urlpatterns = [
    path('v1/', include(router.urls))
]
