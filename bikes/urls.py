from django.urls import path
from .views import AvailableBikesListView, RentBikeView

urlpatterns = [
    path('available/', AvailableBikesListView.as_view(), name='available_bikes'),
    path('rent/<int:pk>/', RentBikeView.as_view(), name='rent_bike'),
]
