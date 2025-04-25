import pytest
from staytrade.providers.api.serializers import RoomTypeMealPlanPriceBulkSerializer


@pytest.mark.django_db
class TestRoomTypeMealPlanPriceBulkSerializer:
    def test_valid_data(self, create_room_type, create_meal_plan):
        data = {
            "room_type": create_room_type.id,
            "meal_plan": create_meal_plan.id,
            "start_date": "2024-01-01",
            "end_date": "2024-01-02",
            "price": "100.00",
        }
        serializer = RoomTypeMealPlanPriceBulkSerializer(data=data)
        assert serializer.is_valid()

    def test_invalid_dates(self, create_room_type, create_meal_plan):
        data = {
            "room_type": create_room_type.id,
            "meal_plan": create_meal_plan.id,
            "start_date": "2024-01-02",
            "end_date": "2024-01-01",
            "price": "100.00",
        }
        serializer = RoomTypeMealPlanPriceBulkSerializer(data=data)
        assert not serializer.is_valid()
