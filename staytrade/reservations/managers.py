from django.db.models import Manager, Count


class BookingManager(Manager):
    def create_with_room_nights(self, check_in, check_out, room_nights):
        """
        Crea un booking y asocia las room_nights
        """
        booking = self.create(check_in=check_in, check_out=check_out, status="pending")
        booking.room_nights.add(*room_nights)
        return booking


class RoomNightManager(Manager):
    def get_availability(self, room_type_id, start_date, end_date):
        """
        Obtiene la ocupación de habitaciones para un período
        """
        return (
            self.filter(
                room_type_id=room_type_id,
                entry_date__lte=end_date,
                departure_date__gte=start_date,
                is_deleted=False,
            )
            .values("entry_date")
            .annotate(occupied_rooms=Count("id"))
        )

    def create_for_period(self, room_type_id, start_date, end_date, owner):
        """
        Crea una RoomNight verificando restricciones de negocio
        """
        return self.create(
            entry_date=start_date,
            departure_date=end_date,
            room_type_id=room_type_id,
            owner=owner,
        )
