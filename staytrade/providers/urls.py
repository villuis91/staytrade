from django.urls import path
from staytrade.providers.views import (
    HotelCreationWizard,
    HotelDetailView,
    MyHotelListView,
    MyAreaView
)

app_name = "providers"
urlpatterns = [
    path("my_area/",  MyAreaView.as_view(), name="my_area"),
    path("my_hotels/", MyHotelListView.as_view(), name="my_hotels_list"),
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
    # path(
    #     "hotels/<int:hotel_id>/tipos-habitacion/nuevo/",
    #     views.RoomTypeCreateView.as_view(),
    #     name="roomtype_create",
    # ),
    # path(
    #     "hotels/<int:hotel_id>/habitaciones/nueva/",
    #     views.RoomCreateView.as_view(),
    #     name="room_create",
    # ),
]
