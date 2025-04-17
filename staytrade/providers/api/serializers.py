from rest_framework import serializers
from staytrade.providers.models import RoomTypeMealPlanPrice, RoomType, MealPlan


class RoomTypeMealPlanPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomTypeMealPlanPrice
        fields = ["room_type", "meal_plan", "start_date", "end_date", "price"]


class RoomTypeMealPlanPriceBulkSerializer(serializers.Serializer):
    room_type = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all())
    meal_plan = serializers.PrimaryKeyRelatedField(queryset=MealPlan.objects.all())
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError(
                "La fecha de inicio debe ser anterior a la fecha final"
            )
        return data
