from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema

from .models import Passenger, Trip, TripToPassenger
from rest_framework import status, serializers
from .serializers import PassengerSerializer, TripSerializer, TripToPassengerSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .tasks import send_email_task


@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_passengers': 'all_passengers/',
        'Search by name for passenger': 'all_passengers/?name=ali',
        'Search by email for passenger': 'all_passengers/?email=ali@gmail.com',
        'Add Passenger': '/add_passenger',
        'Update Passenger': '/update_passenger/pk',
        'Delete Passenger': '/passenger/pk/delete',
        'MiddleWareHeader': request.headers['Custom-Header']
    }
    send_email_task.delay("api page visited")
    return Response(api_urls)


@swagger_auto_schema(method='post', request_body=PassengerSerializer)
@api_view(['POST'])
def add_passenger(request):
    item = PassengerSerializer(data=request.data)

    # validating for already existing data
    if Passenger.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if item.is_valid():
        item.save()
        send_email_task.delay("data added to passenger table")
        return Response(item.data, headers={'MiddleWareHeader': request.headers['Custom-Header']})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_passengers(request):
    # checking for the parameters from the URL
    if request.query_params:
        items = Passenger.objects.filter(**request.query_params.dict())
    else:
        items = Passenger.objects.all()

    # if there is something in items else raise error
    if items:
        serialzer = PassengerSerializer(items, many=True)
        return Response(serialzer.data, headers={'MiddleWareHeader': request.headers['Custom-Header']})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='patch', request_body=PassengerSerializer)
@api_view(['PATCH'])
def update_passenger(request, pk):
    item = Passenger.objects.get(pk=pk)
    item_dict = model_to_dict(item)
    updated_data = request.data
    for index in item_dict:
        if index not in updated_data:
            request.data[index] = item_dict[index]

    data = PassengerSerializer(instance=item, data=updated_data)
    if data.is_valid():
        data.save()
        send_email_task.delay("data updated to passenger table")
        return Response(data.data, headers={'MiddleWareHeader': request.headers['Custom-Header']})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_passenger(request, pk):
    item = get_object_or_404(Passenger, pk=pk)
    item.delete()
    send_email_task.delay("data deleted to trip passenger")
    return Response(status=status.HTTP_202_ACCEPTED)


@swagger_auto_schema(methods=['post'], request_body=TripSerializer)
@api_view(['GET', 'POST'])
def trip_view_get_post(request):
    if request.method == 'GET':
        if request.query_params:
            items = Trip.objects.filter(**request.query_params.dict())
        else:
            items = Trip.objects.all()

        # if there is something in items else raise error
        if items:
            serialzer = TripSerializer(items, many=True)
            return Response(serialzer.data, headers={'MiddleWareHeader': request.headers['Custom-Header']})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        passenger_data = request.data.pop('passenger')
        new_data = request.data
        item = TripSerializer(data=new_data)
        if Trip.objects.filter(**new_data).exists():
            raise serializers.ValidationError('This data already exists')
        if item.is_valid():

            item.save()
            trip_id = Trip.objects.latest('id')

            for index in passenger_data:
                many_to_many_data = {"trip_id": trip_id.id, "passenger_id": index}
                item2 = TripToPassengerSerializer(data=many_to_many_data)
                if item2.is_valid():
                    item2.save()
            send_email_task.delay("data added to trip table")
            return Response(item.data, headers={'MiddleWareHeader': request.headers['Custom-Header']})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(methods=['patch'], request_body=TripSerializer)
@api_view(['PATCH', 'DELETE'])
def trip_view_update_delete(request, pk):
    if request.method == 'PATCH':
        item = Trip.objects.get(pk=pk)
        item_dict = model_to_dict(item)
        updated_data = request.data
        passenger_update_data = updated_data.pop('passenger')
        for index in item_dict:
            if index not in updated_data:
                request.data[index] = item_dict[index]
        data = TripSerializer(instance=item, data=updated_data)
        if data.is_valid():
            data.save()
            passenger_data = TripToPassenger.objects.filter(trip_id=pk)
            bulk_update_count = len(passenger_data)
            passenger_update_data_count = len(passenger_update_data)
            if bulk_update_count == passenger_update_data_count:
                for index in range(passenger_update_data_count):
                    update_relation_data = {"trip_id": pk, "passenger_id": passenger_update_data[index]}
                    item2 = TripToPassengerSerializer(instance=passenger_data[index], data=update_relation_data)
                    if item2.is_valid():
                        item2.save()
            else:
                for data_id in passenger_data:
                    get_object_or_404(TripToPassenger, pk=data_id.id).delete()
                for passenger_id in passenger_update_data:
                    many_to_many_data = {"trip_id": pk, "passenger_id": passenger_id}
                    item2 = TripToPassengerSerializer(data=many_to_many_data)
                    if item2.is_valid():
                        item2.save()
            send_email_task.delay("data updated to trip table")
            return Response(data.data, headers={'MiddleWareHeader': request.headers['Custom-Header']})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        item = get_object_or_404(Trip, pk=pk)
        item.delete()
        send_email_task.delay("data deleted to trip table")
        return Response(status=status.HTTP_202_ACCEPTED)
