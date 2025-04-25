from django.contrib import admin
from staytrade.providers.models import (
    Hotel,
    RoomType,
)

# Common readonly fields
readonly_timestamps = [
    "created_at",
    "updated_at",
]
readonly_timestamps_soft = readonly_timestamps + [
    "deleted_at",
    "restored_at",
    "transaction_id",
]


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    model = Hotel
    readonly_fields = readonly_timestamps_soft + ["created_by"]


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    model = RoomType
    readonly_fields = readonly_timestamps_soft

