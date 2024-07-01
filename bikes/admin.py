from django.contrib import admin
from .models import Bike

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'user', 'rented_until')
    list_filter = ('status',)
    search_fields = ('name', 'user__email')
