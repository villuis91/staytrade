from django.db import transaction
from staytrade.providers.models import RoomType
from .models import RoomNight, RoomNightOwner, Booking
from datetime import timedelta


class RoomAvailabilityService:
    @staticmethod
    def check_availability(room_type_id, start_date, end_date):
        room_type = RoomType.objects.get(id=room_type_id)
        total_rooms = room_type.total_rooms

        existing_nights = RoomNight.objects.get_availability(
            room_type_id, start_date, end_date
        )

        availability = {}
        current_date = start_date
        while current_date <= end_date:
            occupied = next(
                (
                    n["occupied_rooms"]
                    for n in existing_nights
                    if n["entry_date"] == current_date
                ),
                0,
            )
            availability[current_date] = {
                "available": total_rooms - occupied,
                "total": total_rooms,
                "occupied": occupied,
            }
            current_date += timedelta(days=1)

        return availability

    @staticmethod
    def create_room_nights(room_type_id, start_date, end_date, owner_data):
        availability = RoomAvailabilityService.check_availability(
            room_type_id, start_date, end_date
        )

        if any(data["available"] <= 0 for data in availability.values()):
            raise ValueError("No hay disponibilidad suficiente")

        with transaction.atomic():
            owner = RoomNightOwner.objects.create(**owner_data)

            return RoomNight.objects.create_for_period(
                room_type_id, start_date, end_date, owner
            )


class BookingService:
    @staticmethod
    def create_booking(check_in, check_out, room_nights, owner_data):
        with transaction.atomic():
            return Booking.objects.create_with_room_nights(
                check_in, check_out, room_nights
            )
