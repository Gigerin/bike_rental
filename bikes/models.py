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
    rented_from = models.DateTimeField(null=True, blank=True)
    rented_until = models.DateTimeField(null=True, blank=True) #TODO добавить проверку что аренда не в прошлом

    def save(self, *args, **kwargs):
        if self.status == 'rented':
            if not self.rented_from or not self.rented_until:
                raise ValueError("Не указана даты аренды.")
            if self.rented_until < self.rented_from:
                raise ValueError("Дата начала аренды позже даты окончания.")
            if is_in_past(self.rented_until):
                raise ValueError("Дата конца аренды в прошлом.")
        if self.status == 'available':
            if self.user:
                raise ValueError("Невозможно арендовать без арендатора.")
            if self.rented_until or self.rented_from:
                raise ValueError("Необходимо удалить время аренды.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RentalEvent(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rented_from = models.DateTimeField()
    rented_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} rented {self.bike.id} from {self.rented_from} to {self.rented_until}'
