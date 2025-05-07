from django.db.models import Manager, Count


class BookingManager(Manager):
    def create_pre_booking(self, check_in, check_out):
        """
        Create a booking previous to be paid.
        """
        booking = self.create(
            check_in=check_in, check_out=check_out, status=self.status.PENDING
        )
        return booking

    def confirm_booking(self, booking_id):
        # TODO: When confirmed, create associated room nights (Check once again the status)
        return self.filter(id=booking_id).update(status=self.status.CONFIRMED)

    def cancel_booking(self, booking_id):
        return self.filter(id=booking_id).update(status=self.status.CANCELLED)


class RoomNightManager(Manager):
    def get_availability(self, room_type, start_date, end_date):
        """
        Obtiene la ocupación de habitaciones para un período
        """
        return (
            self.filter(
                room_type=room_type,
                entry_date__lte=end_date,
                departure_date__gte=start_date,
                deleted_at=None,
            )
            .values("entry_date")
            .annotate(occupied_rooms=Count("id"))
        )

    def create_for_period(self, room_type, start_date, end_date, owner):
        """
        Crea una RoomNight verificando restricciones de negocio
        """
        return self.create(
            entry_date=start_date,
            departure_date=end_date,
            room_type=room_type,
            owner=owner,
        )

    def change_owner(self, room_nights, new_owner):
        return self.filter(id__in=room_nights).update(owner=new_owner)
