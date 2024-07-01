from datetime import timedelta

from django.utils import timezone
from django.db import models
from bike_rental import settings


class Bike(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
    ]

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    rented_from = models.DateTimeField(null=True, blank=True, default=timezone.now())
    rented_until = models.DateTimeField(null=True, blank=True, default=timezone.now()+timedelta(1) ) #TODO добавить проверку что аренда не в прошлом

    def save(self, *args, **kwargs):
        if self.status == 'rented':
            if self.rented_until < self.rented_from:
                raise ValueError("Дата начала аренды позже даты окончания.")
            if self.rented_until < timezone.now():
                raise ValueError("Дата конца аренды в прошлом.")
        if self.status == 'available':
            if self.user:
                raise ValueError("Невозможно арендовать без арендатора.")
            if self.rented_until or self.rented_from:
                raise ValueError("Необходимо удалить время аренды.")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name