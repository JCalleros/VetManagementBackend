from django.urls import path, include
from .views import CreateUserView, CurrentUserView


urlpatterns = [
    path('', CreateUserView.as_view(), name='create-user'),
    path('me/', CurrentUserView.as_view(), name='current-user')
]
