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
    rented_until = models.DateTimeField(null=True, blank=True) #TODO добавить проверку что аренда не в прошлом

    def save(self, *args, **kwargs):
        if self.status == 'rented' and not self.user:
            raise ValueError("Cannot rent a bike without a user.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name