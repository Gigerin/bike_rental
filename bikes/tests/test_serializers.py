from decimal import Decimal

import pytest
from datetime import datetime
from bikes.serializers import BikeSerializer, RentalEventSerializer
from bikes.models import Bike, RentalEvent

@pytest.mark.django_db
def test_bike_serializer(rented_bike, user):
    serializer = BikeSerializer(rented_bike)
    data = serializer.data

    assert data['id'] == rented_bike.id
    assert data['name'] == rented_bike.name
    assert data['status'] == rented_bike.status
    assert Decimal(data['price']) == Decimal(rented_bike.price)
    assert data['user'] == rented_bike.user.id
    assert data['rented_from'].rstrip('Z') == rented_bike.rented_from.isoformat()
    assert data['rented_until'].rstrip('Z') == rented_bike.rented_until.isoformat()

@pytest.mark.django_db
def test_rental_event_serializer(rental_event):
    serializer = RentalEventSerializer(rental_event)
    data = serializer.data

    assert data['bike'] == rental_event.bike.id
    assert data['user'] == rental_event.user.id
    assert data['rented_from'].rstrip('Z') == rental_event.rented_from.isoformat()
    assert data['rented_until'].rstrip('Z') == rental_event.rented_until.isoformat()

@pytest.mark.django_db
def test_bike_serializer_create(custom_available_bike, user, future_date):
    bike_data = {
        'name': 'Test Bike',
        'status': 'rented',
        'price': 1200,
        'user': user.id,
        'rented_from': future_date['rented_from'],
        'rented_until': future_date['rented_until'],
    }
    print(bike_data)
    serializer = BikeSerializer(data=bike_data)
    if serializer.is_valid():
        print("puk")
        pass
    else:
        print(serializer.errors)

    assert serializer.is_valid()
    bike = serializer.save()

    assert bike.name == bike_data['name']
    assert bike.status == bike_data['status']
    assert bike.price == bike_data['price']
    assert bike.user == user
    assert bike.rented_from == future_date['rented_from']
    assert bike.rented_until == future_date['rented_until']

@pytest.mark.django_db
def test_rental_event_serializer_create(available_bike, user, future_date):
    rental_event_data = {
        'bike': available_bike.id,
        'user': user.id,
        'rented_from': future_date['rented_from'],
        'rented_until': future_date['rented_until'],
    }

    serializer = RentalEventSerializer(data=rental_event_data)
    assert serializer.is_valid()
    rental_event = serializer.save()

    assert rental_event.bike == available_bike
    assert rental_event.user == user
    assert rental_event.rented_from == future_date['rented_from']
    assert rental_event.rented_until == future_date['rented_until']
