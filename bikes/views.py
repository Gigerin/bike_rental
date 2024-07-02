from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes

from .models import Bike, RentalEvent
from .serializers import BikeSerializer, RentalEventSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def available_bikes(request):
    bikes = Bike.objects.filter(status='available')
    serializer = BikeSerializer(bikes, many=True)
    return Response(serializer.data)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def rent_bike(request, pk):
    try:
        bike = Bike.objects.get(pk=pk)
    except Bike.DoesNotExist:
        return Response({"error": "Велосипед не найден."}, status=status.HTTP_404_NOT_FOUND)

    if bike.status != 'available':
        return Response({"error": "Велосипед уже арендован."}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data.copy()
    data['status'] = 'rented'
    data['user'] = request.user.id

    # Update bike status
    bike_serializer = BikeSerializer(bike, data=data, partial=True)
    if bike_serializer.is_valid():
        bike_serializer.save()
    else:
        return Response(bike_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Create rental event
    rental_event_data = {
        'bike': bike.id,
        'user': request.user.id,
        'rented_from': data.get('rented_from'),
        'rented_until': data.get('rented_until')
    }
    rental_event_serializer = RentalEventSerializer(data=rental_event_data)
    if rental_event_serializer.is_valid():
        rental_event_serializer.save()
    else:
        return Response(rental_event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(bike_serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def return_bike(request, pk):
    try:
        bike = Bike.objects.get(pk=pk)
    except Bike.DoesNotExist:
        return Response({"error": "Велосипед не найден."}, status=status.HTTP_404_NOT_FOUND)

    if bike.status != 'rented':
        return Response({"error": "Велосипед уже свободен."}, status=status.HTTP_400_BAD_REQUEST)
    data = request.data
    data['status'] = 'available'
    data['user'] = None
    data['rented_until'] = None
    data['rented_from'] = None

    serializer = BikeSerializer(bike, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)