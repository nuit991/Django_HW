from django.urls import path
from .views import home, gym_data_api

urlpatterns = [
    path('', home, name = 'home'),
    path('api/gym-data/', gym_data_api, name = 'gym_data_api'),
]
