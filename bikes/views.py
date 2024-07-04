from datetime import timezone, datetime
import pytz
from dateutil import parser
from django.utils.dateparse import parse_datetime
from bikes.utils import cast_to_aware, calculate_total_price
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes

from bikes.tasks import send_bill
from .models import Bike, RentalEvent
from .serializers import BikeSerializer, RentalEventSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
def available_bikes(request):
    "Возвращает список доступных велосипедов"
    bikes = Bike.objects.filter(status="available")
    serializer = BikeSerializer(bikes, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_rent_history(request):
    "Возвращает список аренд текущего пользователя"
    user = request.user
    bikes = RentalEvent.objects.filter(user=user)
    serializer = RentalEventSerializer(bikes, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def rent_bike(request, pk):
    """
    Арендует велосипед по pk
    :param request:
    :param pk: ID велосипеда
    :return: данные об успешно арендованном велосипеде
    """
    try:
        bike = Bike.objects.get(pk=pk)
    except Bike.DoesNotExist:
        return Response(
            {"error": "Велосипед не найден."}, status=status.HTTP_404_NOT_FOUND
        )

    if bike.status != "available":
        return Response(
            {"error": "Велосипед уже арендован."}, status=status.HTTP_400_BAD_REQUEST
        )

    if Bike.objects.filter(user_id=request.user.id).exists():
        return Response(
            {"error": "Арендовать можно только один велосипед."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = request.data.copy()
    data["status"] = "rented"
    data["user"] = request.user.id
    bike_serializer = BikeSerializer(bike, data=data, partial=True)
    if bike_serializer.is_valid():
        bike_serializer.save()
    else:
        return Response(bike_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(bike_serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def return_bike(request, pk):
    """
    Возвращает велосипед, формирует ивень аренды, отправляет счет на почту
    :param request:
    :param pk: ID велосипеда
    :return: данные о велосипеде
    """
    try:
        bike = Bike.objects.get(pk=pk)
    except Bike.DoesNotExist:
        return Response(
            {"error": "Велосипед не найден."}, status=status.HTTP_404_NOT_FOUND
        )
    if bike.status != "rented":
        return Response(
            {"error": "Велосипед уже свободен."}, status=status.HTTP_400_BAD_REQUEST
        )
    rental_event_data = {
        "bike": bike.id,
        "user": request.user.id,
        "rented_from": bike.rented_from,
        "rented_until": datetime.now(timezone.utc),
        "total_price": calculate_total_price(bike),
    }
    rental_event_serializer = RentalEventSerializer(data=rental_event_data)
    if rental_event_serializer.is_valid():
        rental_event_serializer.save()
        send_bill.delay(rental_event_serializer.data)
    else:
        return Response(
            rental_event_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    data = request.data
    data["status"] = "available"
    data["user"] = None
    data["rented_from"] = None

    serializer = BikeSerializer(bike, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
