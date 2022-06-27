from django.contrib import admin
from .models import Passenger,Trip,TripToPassenger
# Register your models here.
admin.site.register(Passenger)
admin.site.register(Trip)
admin.site.register(TripToPassenger)