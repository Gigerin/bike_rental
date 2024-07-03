from datetime import datetime

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from bikes.models import Bike, RentalEvent

@pytest.mark.django_db
def test_available_bikes(api_client, available_bike):
    response = api_client.get('/api/bikes/available/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['status'] == 'available'

@pytest.mark.django_db
def test_get_rent_history(auth_client, rented_bike, rental_event):
    response = auth_client.get('/api/bikes/get_rent_history/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['bike'] == rented_bike.id

@pytest.mark.django_db
def test_rent_bike_success(auth_client, available_bike, future_date):
    response = auth_client.put(f'/api/bikes/rent/{available_bike.id}/', future_date)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'rented'

@pytest.mark.django_db
def test_rent_bike_one_user_two_bikes(auth_client, custom_available_bike,  future_date):
    bike1 = custom_available_bike(name="Ariel")
    bike2 = custom_available_bike(name="Stels")
    response = auth_client.put(f'/api/bikes/rent/{bike1.id}/', future_date)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'rented'
    response = auth_client.put(f'/api/bikes/rent/{bike2.id}/', future_date)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'Арендовать можно только один велосипед.'

@pytest.mark.django_db
def test_rent_bike_not_found(auth_client, available_bike, future_date):
    response = auth_client.put('/api/bikes/rent/999/', future_date)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['error'] == 'Велосипед не найден.'

@pytest.mark.django_db
def test_rent_bike_already_rented(auth_client, rented_bike, future_date):
    response = auth_client.put(f'/api/bikes/rent/{rented_bike.id}/', future_date)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'Велосипед уже арендован.'

@pytest.mark.django_db
def test_return_bike_success(auth_client, rented_bike):
    response = auth_client.put(f'/api/bikes/return/{rented_bike.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'available'

@pytest.mark.django_db
def test_return_bike_not_found(auth_client):
    response = auth_client.put('/api/bikes/return/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['error'] == 'Велосипед не найден.'

@pytest.mark.django_db
def test_return_bike_not_rented(auth_client, available_bike):
    response = auth_client.put(f'/api/bikes/return/{available_bike.id}/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'Велосипед уже свободен.'
