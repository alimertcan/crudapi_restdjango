from .models import Passenger,Trip
from rest_framework import serializers


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ('name', 'status', 'email')

    # def to_representation(self, value):
    #     return value.email



class TripSerializer(serializers.ModelSerializer):
    passenger = PassengerSerializer(many=True)
    class Meta:
        model = Trip
        fields = ('total_distance', 'start_time', 'end_time','passenger')
