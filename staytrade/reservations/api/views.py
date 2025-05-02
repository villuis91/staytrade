from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from staytrade.reservations.models import RoomNight, Booking
from .serializers import (
    RoomNightSerializer,
    BookingSerializer,
    RoomNightOwnerSerializer,
)
from staytrade.reservations.services import RoomAvailabilityService, BookingService


class RoomNightViewSet(viewsets.ModelViewSet):
    queryset = RoomNight.objects.all()
    serializer_class = RoomNightSerializer

    @action(detail=False, methods=["post"])
    def create_with_owner(self, request):
        try:
            owner_serializer = RoomNightOwnerSerializer(data=request.data.get("owner"))
            if not owner_serializer.is_valid():
                return Response(
                    owner_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            room_night = RoomAvailabilityService.create_room_nights(
                room_type_id=request.data.get("room_type"),
                start_date=request.data.get("entry_date"),
                end_date=request.data.get("departure_date"),
                owner_data=owner_serializer.validated_data,
            )

            return Response(
                RoomNightSerializer(room_night).data, status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @action(detail=False, methods=["post"])
    def create_with_room_nights(self, request):
        try:
            booking = BookingService.create_booking(
                check_in=request.data.get("check_in"),
                check_out=request.data.get("check_out"),
                room_nights=request.data.get("room_nights"),
                owner_data=request.data.get("owner"),
            )

            return Response(
                BookingSerializer(booking).data, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        try:
            booking = self.get_object()
            booking.status = request.data.get("status")
            booking.save()

            return Response(BookingSerializer(booking).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
