# tests/conftest.py
import pytest
from datetime import date
from decimal import Decimal
from staytrade.providers.models import Hotel, RoomType, MealPlan, RoomTypeMealPlanPrice


@pytest.fixture
def create_hotel(db, django_user_model):
    user = django_user_model.objects.create(username="test_user")
    return Hotel.objects.create(
        created_by=user, name="Test Hotel", description="Test Description", stars=4
    )


@pytest.fixture
def create_room_type(db, create_hotel):
    return RoomType.objects.create(
        name="Test Room",
        description="Test Description",
        hotel=create_hotel,
        created_by=create_hotel.created_by,
    )


@pytest.fixture
def create_meal_plan(db, create_hotel):
    return MealPlan.objects.create(
        hotel=create_hotel, name="Test Meal Plan", details="Test Details"
    )


@pytest.fixture
def create_price(db, create_room_type, create_meal_plan):
    return RoomTypeMealPlanPrice.objects.create(
        room_type=create_room_type,
        meal_plan=create_meal_plan,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 2),
        price=Decimal("100.00"),
    )
