from django.contrib import admin
from staytrade.providers.models import (
    Hotel,
    Room,
    RoomNight,
    RoomAvailability,
    RoomTypeAvailability,
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


class InlineRoomAvailability(admin.TabularInline):
    model = RoomAvailability


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    model = Room
    readonly_fields = readonly_timestamps_soft
    inlines = [InlineRoomAvailability]


class InlineRoomTypeAvailability(admin.TabularInline):
    model = RoomTypeAvailability


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    model = RoomType
    readonly_fields = readonly_timestamps_soft
    inlines = [InlineRoomTypeAvailability]


@admin.register(RoomNight)
class RoomNightAdmin(admin.ModelAdmin):
    model = RoomNight
    readonly_fields = readonly_timestamps_soft
