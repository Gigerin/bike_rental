from django.urls import path
from .views import available_bikes, rent_bike, return_bike, get_rent_history

urlpatterns = [
    path('available/', available_bikes, name='available_bikes'),
    path('rent/<int:pk>/', rent_bike, name='rent_bike'),
    path('return/<int:pk>/', return_bike, name='rent_bike'),
    path('get_rent_history/', get_rent_history, name='get_rent_history'),
]
