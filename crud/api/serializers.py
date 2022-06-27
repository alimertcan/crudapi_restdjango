from .models import Passenger,Trip,TripToPassenger
from rest_framework import serializers


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ('name', 'status', 'email')

    def to_representation(self, value):
        return value.pk



class TripSerializer(serializers.ModelSerializer):
    passenger = PassengerSerializer(many=True,read_only=True)

    class Meta:
        model = Trip
        fields = ('total_distance', 'start_time', 'end_time','passenger')


class TripToPassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripToPassenger
        fields = ('trip_id', 'passenger_id')