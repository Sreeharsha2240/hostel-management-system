from django.contrib import admin

from .models import Bed, Hostel, Room


class RoomInline(admin.TabularInline):
    model = Room
    extra = 1


class BedInline(admin.TabularInline):
    model = Bed
    extra = 0
    readonly_fields = ("label",)


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ("name", "hostel_type", "is_active")
    search_fields = ("name",)
    list_filter = ("hostel_type", "is_active")
    inlines = (RoomInline,)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "room_number",
        "hostel",
        "floor",
        "room_type",
        "capacity",
        "fee_amount",
    )
    list_filter = ("hostel", "floor", "room_type")
    search_fields = ("room_number", "hostel__name")
    inlines = (BedInline,)


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ("label", "room", "status")
    list_filter = ("status", "room__hostel")
    search_fields = ("label", "room__room_number", "room__hostel__name")
