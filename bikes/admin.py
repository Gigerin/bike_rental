from django.contrib import admin
from .models import Bike, RentalEvent


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'user')
    list_filter = ('status',)
    search_fields = ('name', 'user__email')

@admin.register(RentalEvent)
class RentalEventAdmin(admin.ModelAdmin):
    list_display = ('bike', 'user', 'rented_from', 'rented_until')
    list_filter = ('bike',)
    search_fields = ('name', 'user__email', 'bike')
