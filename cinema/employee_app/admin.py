from django.contrib import admin
from employee_app.models import *



class ProjectionInLine(admin.StackedInline):
	model = Projection
	extra = 1

class MovieAdmin(admin.ModelAdmin):
	inlines = [ProjectionInLine]
	list_display = ['title', 'length', 'genre', 'minimal_age']
	search_fields = ['title']
	list_filter = ['length', 'genre', 'minimal_age']

admin.site.register(Movie, MovieAdmin)


class ClientAdmin(admin.ModelAdmin):
	list_display = ['name', 'surname', 'phone', 'email']
	search_fields = ['name', 'surname']


admin.site.register(Client, ClientAdmin)

class ReservationAdmin(admin.ModelAdmin):
	list_display = ['client', 'projection','seat_number', 'received']
	search_fields = ['client']
	list_filter = ['client', 'projection']

admin.site.register(Reservation, ReservationAdmin)


class RoomAdmin(admin.ModelAdmin):
	list_display = ['room_number', 'seats_number', 'status']
	list_filter = ['status']

admin.site.register(Room, RoomAdmin)
