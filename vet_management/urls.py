from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="vetSystem API",
      default_version='v1',
      description="vetSystem API Documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/pets/', include('pets.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/appointments/', include('appointments.urls'))
]

if settings.DEBUG:
   urlpatterns += [
      path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='scheme-swagger'),
      path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   ]
