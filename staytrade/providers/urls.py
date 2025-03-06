from django.urls import path
from staytrade.providers.views import HotelCreationWizard, HotelDetailView

app_name = "providers"
# urls.py
urlpatterns = [
    # path("hotels/", views.HotelListView.as_view(), name="hotel_list"),
    path("hotels/new/", HotelCreationWizard.as_view(), name="hotel_create_wizard"),
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
