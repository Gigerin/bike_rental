from rest_framework import serializers
from .models import Bike


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ['id', 'name', 'status', 'user', 'rented_until', 'rented_from']

    def validate(self, data):
        print(data)
        if data.get('status') == 'rented' and not data.get('user'):
            raise serializers.ValidationError("Cannot rent a bike without a user.")
        return data
