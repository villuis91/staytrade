from rest_framework import serializers
from staytrade.reservations.models import RoomNight, RoomNightOwner, Booking


class RoomNightOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomNightOwner
        fields = ["first_name", "last_name", "phone_number", "national_identifier"]


class RoomNightSerializer(serializers.ModelSerializer):
    owner = RoomNightOwnerSerializer()
    entry_date = serializers.DateField()
    departure_date = serializers.DateField()

    class Meta:
        model = RoomNight
        fields = ["id", "entry_date", "departure_date", "room_type", "owner"]

    def validate(self, data):
        """
        Validar que la fecha de entrada sea anterior a la de salida
        """
        if data["entry_date"] >= data["departure_date"]:
            raise serializers.ValidationError(
                {"error": "La fecha de entrada debe ser anterior a la de salida"}
            )
        return data


class BookingSerializer(serializers.ModelSerializer):
    room_nights = RoomNightSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "check_in", "check_out", "status", "room_nights"]
