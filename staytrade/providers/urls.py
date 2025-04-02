from django.urls import path
from staytrade.providers.views.hotels import (
    HotelCreationWizard,
    HotelDetailView,
    HotelDeleteView,
    HotelUpdateView,
    MyHotelsListView,
)
from staytrade.providers.views.room_types import (
    RoomTypeCreationWizardView,
    RoomTypeDeleteView,
    RoomTypeDetailView,
    RoomTypeUpdateView,
    MyHotelRoomsListView,
)
from staytrade.providers.views.misc import (
    MyAreaView,
    HotelManagementView,
)
from staytrade.providers.views.meal_plans import (
    MealPlanListView,
    MealPlanCreateView,
    MealPlanDetailView,
    MealPlanUpdateView,
    MealPlanDeleteView,
)

app_name = "providers"
urlpatterns = [
    # Main area
    path("my_area/", MyAreaView.as_view(), name="my_area"),
    # Hotels
    path("my_hotels/", MyHotelsListView.as_view(), name="my_hotels_list"),
    path(
        "hotels/new/",
        HotelCreationWizard.as_view(),
        name="hotel_create_wizard_default",
    ),
    path(
        "hotels/new/<str:step>/",
        HotelCreationWizard.as_view(),
        name="hotel_create_wizard",
    ),
    path(
        "hotels/management/<int:pk>/",
        HotelManagementView.as_view(),
        name="hotel_management",
    ),
    path("hotels/<int:pk>/", HotelDetailView.as_view(), name="hotel_detail"),
    path("hotels/delete/<int:pk>/", HotelDeleteView.as_view(), name="hotel_delete"),
    path("hotels/update/<int:pk>/", HotelUpdateView.as_view(), name="hotel_update"),
    # Room types
    path(
        "roomtypes/new/<int:hotel_id>/",
        RoomTypeCreationWizardView.as_view(),
        name="room_type_create_wizard_default",
    ),
    path(
        "roomtypes/new/<int:hotel_id>/<str:step>/",
        RoomTypeCreationWizardView.as_view(),
        name="room_type_create_wizard",
    ),
    path(
        "my_rooms/<int:hotel_id>/",
        MyHotelRoomsListView.as_view(),
        name="my_hotel_rooms_list",
    ),
    path("roomtypes/<int:pk>/", RoomTypeDetailView.as_view(), name="roomtype_detail"),
    path(
        "roomtypes/delete/<int:pk>/",
        RoomTypeDeleteView.as_view(),
        name="roomtype_delete",
    ),
    path(
        "roomtypes/update/<int:pk>/",
        RoomTypeUpdateView.as_view(),
        name="roomtype_update",
    ),
    # Meal plans
    path(
        "mealplan/list/<int:hotel_id>/",
        MealPlanListView.as_view(),
        name="meal_plan_list",
    ),
    path(
        "mealplan/create/<int:hotel_id>/",
        MealPlanCreateView.as_view(),
        name="meal_plan_create",
    ),
    path(
        "mealplan/detail/<int:pk>/",
        MealPlanDetailView.as_view(),
        name="meal_plan_detail",
    ),
    path(
        "mealplan/update/<int:pk>/",
        MealPlanUpdateView.as_view(),
        name="meal_plan_update",
    ),
    path(
        "mealplan/delete/<int:pk>/",
        MealPlanDeleteView.as_view(),
        name="meal_plan_delete",
    ),
]
