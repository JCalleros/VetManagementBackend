from django.urls import path, include
from .views import CreateUserView, CurrentUserView


urlpatterns = [
    path('v1/users/', CreateUserView.as_view(), name='create-user'),
    path('v1/users/me/', CurrentUserView.as_view(), name='current-user')
]
