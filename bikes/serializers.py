from rest_framework import serializers
from .models import Bike, RentalEvent


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ['id', 'name', 'status', 'price', 'user', 'rented_until', 'rented_from']

    def validate(self, data):
        if data.get('status') == 'rented' and not data.get('user'):
            raise serializers.ValidationError("Cannot rent a bike without a user.")
        return data

class RentalEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalEvent
        fields = ['bike', 'user', 'rented_until', 'rented_from']

    def validate(self, data):
        print(data)
        return data