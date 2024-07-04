import pytest
from django.utils import timezone
from datetime import timedelta, datetime
from bikes.models import Bike, RentalEvent
from users.models import User


@pytest.mark.django_db
def test_bike_status_available_with_user():
    user = User.objects.create(email="test@example.com", password="testpass")
    bike = Bike(name="Test Bike", status="available", user=user)
    with pytest.raises(
        ValueError, match="Невозможно создать свободный велосипед с пользователем."
    ):
        bike.save()


@pytest.mark.django_db
def test_bike_status_available_with_rental_dates():
    bike = Bike(name="Test Bike", status="available", rented_from=timezone.now())
    with pytest.raises(ValueError, match="Необходимо удалить время аренды."):
        bike.save()


@pytest.mark.django_db
def test_bike_save_successful():
    bike = Bike(name="Test Bike", status="available", price=1000)
    print(bike.rented_from)
    bike.save()
    assert Bike.objects.count() == 1


@pytest.mark.django_db
def test_rental_event_creation():
    user = User.objects.create(email="test@example.com", password="testpass")
    bike = Bike.objects.create(name="Test Bike", status="available", price=1000)
    rented_from = timezone.now()
    rented_until = timezone.now() + timedelta(days=1)
    rental_event = RentalEvent.objects.create(
        bike=bike,
        user=user,
        rented_from=rented_from,
        rented_until=rented_until,
        total_price=1000,
    )
    assert RentalEvent.objects.count() == 1
    assert (
        str(rental_event)
        == f"{user.email} rented {bike.id} from {rental_event.rented_from} to {rental_event.rented_until}"
    )
