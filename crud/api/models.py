from django.db import models
# Create your models here.
class Passenger(models.Model):
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=150)
    status = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)



class Trip(models.Model):
    total_distance = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    passenger = models.ManyToManyField(Passenger,blank=True,through='TripToPassenger')



class TripToPassenger(models.Model):
    passenger_id = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)