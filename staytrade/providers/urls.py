from django.urls import path
from staytrade.providers.views import (
    HotelCreationWizard,
    HotelDetailView,
    HotelDeleteView,
    HotelUpdateView,
    MyHotelsListView,
    MyAreaView,
    RoomTypeCreationWizardView,
    RoomTypeDeleteView,
    MyRoomTypesListView
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
    path("roomtypes/<int:pk>/", HotelDetailView.as_view(), name="roomtype_detail"),
    path(
        "roomtypes/delete/<int:pk>/", HotelDeleteView.as_view(), name="roomtype_delete"
    ),
    path(
        "roomtypes/update/<int:pk>/", HotelUpdateView.as_view(), name="roomtype_update"
    ),
    # Room nights
]
