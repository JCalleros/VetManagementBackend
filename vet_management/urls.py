from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/pets/', include('pets.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/appointments/', include('appointments.urls'))
]

admin.site.site_header = "Vet Management Admin"
admin.site.site_title = "Vet Management Admin Portal"
admin.site.index_title = "Welcome to Vet Management Admin Portal"