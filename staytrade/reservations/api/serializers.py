from rest_framework import serializers
from staytrade.reservations.models import RoomNight, RoomNightOwner, Booking


class RoomNightOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomNightOwner
        fields = ["first_name", "last_name", "phone_number", "national_identifier"]


class RoomNightSerializer(serializers.ModelSerializer):
    owner = RoomNightOwnerSerializer()

    class Meta:
        model = RoomNight
        fields = ["id", "entry_date", "departure_date", "room_type", "owner"]


class BookingSerializer(serializers.ModelSerializer):
    room_nights = RoomNightSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "check_in", "check_out", "status", "room_nights"]
