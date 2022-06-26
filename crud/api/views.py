from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema

from .models import Passenger, Trip
from rest_framework import status, serializers, viewsets
from .serializers import PassengerSerializer, TripSerializer
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
    return Response(status=status.HTTP_202_ACCEPTED)


@swagger_auto_schema(methods=['post'], request_body=TripSerializer)
@api_view(['GET', 'POST'])
def trip_view_get_post(request):
    if request.method == 'GET':
        if request.query_params:
            items = Trip.objects.filter(**request.query_params.dict())
        else:
            items = Trip.objects.all()
        for i in items:
            print(i.passenger)
            print(type(i))

        # if there is something in items else raise error
        if items:
            serialzer = TripSerializer(items, many=True)
            print(serialzer.data)
            return Response(serialzer.data, headers={'MiddleWareHeader': request.headers['Custom-Header']})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        new_data = request.data
        new_data = parse_passenger(new_data)
        item = TripSerializer(data=new_data)
        print(item, "222222")
        # validating for already existing data
        if Trip.objects.filter(**new_data).exists():
            raise serializers.ValidationError('This data already exists')
        print(3)
        print(item)
        if item.is_valid():
            print(4)
            item.save()
            return Response(item.data, headers={'MiddleWareHeader': request.headers['Custom-Header']})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


def parse_passenger(data):
    new_list = []

    for index in data['passenger']:
        new_list.append(get_object_or_404(Passenger, email=index))
    print(new_list)
    data['passenger'] = new_list
    return data


@swagger_auto_schema(methods=['patch'], request_body=TripSerializer)
@api_view(['PATCH', 'DELETE'])
def trip_view_update_delete(request, pk):
    if request.method == 'PATCH':
        item = Trip.objects.get(pk=pk)
        print(item)
        item_dict = model_to_dict(item)
        print(item_dict)
        updated_data = request.data
        print(updated_data, 3333)
        for index in item_dict:
            if index not in updated_data:
                request.data[index] = item_dict[index]
        updated_data = parse_passenger(updated_data)
        data = TripSerializer(instance=item, data=updated_data)
        if data.is_valid():
            data.save()
            return Response(data.data, headers={'MiddleWareHeader': request.headers['Custom-Header']})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        item = get_object_or_404(Trip, pk=pk)
        item.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
