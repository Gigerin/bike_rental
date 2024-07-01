from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes

from .models import Bike
from .serializers import BikeSerializer
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
        return Response({"error": "Bike not found."}, status=status.HTTP_404_NOT_FOUND)

    if bike.status != 'available':
        return Response({"error": "Bike is already rented."}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    data['status'] = 'rented'
    data['user'] = request.user.id

    serializer = BikeSerializer(bike, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)