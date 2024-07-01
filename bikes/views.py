from rest_framework import generics, status
from .models import Bike
from .serializers import BikeSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class AvailableBikesListView(generics.ListAPIView):
    queryset = Bike.objects.filter(status='available')
    serializer_class = BikeSerializer


class RentBikeView(generics.UpdateAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        bike = self.get_object()
        if bike.status != 'available':
            return Response({"error": "Bike is already rented."}, status=status.HTTP_400_BAD_REQUEST)

        bike.status = 'rented'
        bike.user = request.user
        bike.rented_until = request.data.get('rented_until')
        bike.save()

        return Response(BikeSerializer(bike).data)