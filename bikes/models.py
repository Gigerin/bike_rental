from datetime import timedelta, datetime, timezone
from django.db import models
from bike_rental import settings
from bikes.utils import is_in_past
from users.models import User


class Bike(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
    ]

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    rented_from = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == 'rented':
            if not self.user:
                raise ValueError('Невозможно арендовать велосипед без арендатора')
            if self.rented_from:
                if is_in_past(self.rented_from):
                    raise ValueError('Время аренды в прошлом.')
            else:
                self.rented_from = datetime.now(timezone.utc)
        if self.status == 'available':
            if self.user:
                raise ValueError("Невозможно создать свободный велосипед с пользователем.")
            if self.rented_from:
                raise ValueError("Необходимо удалить время аренды.")
        if not self.price:
            raise ValueError("Укажите цену.")
        if self.price <= 0:
            raise ValueError("Цена должна быть больше нуля.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RentalEvent(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rented_from = models.DateTimeField()
    rented_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f'{self.user.email} rented {self.bike.id} from {self.rented_from} to {self.rented_until}'
