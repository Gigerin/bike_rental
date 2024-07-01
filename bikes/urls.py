from django.urls import path
from .views import available_bikes, rent_bike

urlpatterns = [
    path('available/', available_bikes, name='available_bikes'),
    path('rent/<int:pk>/', rent_bike, name='rent_bike'),
]
