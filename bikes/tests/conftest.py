# conftest.py
from datetime import datetime, timezone
from dateutil import parser
import pytest
from rest_framework.test import APIClient
from users.models import User
from bikes.models import Bike, RentalEvent


@pytest.fixture
def user(db):
    user = User.objects.create_user(
        name="John Doe", email="test@example.com", password="password123"
    )
    user.save()
    return user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def future_date():
    rent_data = {
        "rented_from": parser.isoparse("2025-08-01T20:57:12.114502Z"),
        "rented_until": parser.isoparse("2025-10-01T20:57:12.114502Z"),
    }
    return rent_data


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def custom_available_bike(db):
    def create_bike(name="Ariel", status="available", price=1000):
        return Bike.objects.create(name=name, status=status, price=price)

    return create_bike


@pytest.fixture
def available_bike(db):
    bike = Bike.objects.create(status="available", price=1000)
    return bike


@pytest.fixture
def rented_bike(db, user):
    rented_from = datetime.strptime(
        "2025-08-01T20:57:12.114502", "%Y-%m-%dT%H:%M:%S.%f"
    )
    bike = Bike.objects.create(
        status="rented", user=user, price=1000, rented_from=rented_from
    )
    return bike


@pytest.fixture
def rental_event(db, user, rented_bike):
    rented_from = datetime.strptime(
        "2025-08-01T20:57:12.114502", "%Y-%m-%dT%H:%M:%S.%f"
    )
    rented_until = datetime.strptime(
        "2025-10-01T20:57:12.114502", "%Y-%m-%dT%H:%M:%S.%f"
    )
    rental_event = RentalEvent.objects.create(
        user=user,
        bike=rented_bike,
        rented_from=rented_from,
        rented_until=rented_until,
        total_price=1000,
    )
    return rental_event
