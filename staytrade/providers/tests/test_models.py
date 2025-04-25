# tests/test_models.py
import pytest
from django.core.exceptions import ValidationError
from datetime import date
from decimal import Decimal
from staytrade.providers.models import Hotel, RoomType, MealPlan, RoomTypeMealPlanPrice


@pytest.mark.django_db
class TestRoomTypeMealPlanPrice:
    def test_create_price_valid_dates(
        self, create_hotel, create_room_type, create_meal_plan
    ):
        price = RoomTypeMealPlanPrice.objects.create(
            room_type=create_room_type,
            meal_plan=create_meal_plan,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 2),
            price=Decimal("100.00"),
        )
        assert price.id is not None

    def test_create_price_invalid_dates(self, create_room_type, create_meal_plan):
        with pytest.raises(ValidationError):
            RoomTypeMealPlanPrice.objects.create(
                room_type=create_room_type,
                meal_plan=create_meal_plan,
                start_date=date(2024, 1, 2),
                end_date=date(2024, 1, 1),
                price=Decimal("100.00"),
            )
