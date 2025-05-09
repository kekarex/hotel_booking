from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'kind', 'price')  # убрали is_available
    list_filter = ('kind',)                     # убрали is_available
    search_fields = ('number',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'created_at')
    list_filter = ('check_in', 'check_out')
    search_fields = ('user__username', 'room__number')