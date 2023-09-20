from django.shortcuts import render, get_object_or_404
from rest_framework. response import Response 
from .models import *
from .serializers import *
from rest_framework.decorators import api_view

"""This view returns a list of all events."""
@api_view(['GET'])
def eventList (request): 
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True) 
    return Response (serializer.data)

"""This view returns the details of a specific event."""
@api_view(['GET'])
def eventDetail(request, pk):
    events = Event.objects.get(id=pk)
    serializer = EventSerializer(events, many=False) 
    return Response (serializer.data)


"""This view creates a new event. """
@api_view(['POST'])
def eventCreate(request) :
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response (serializer.data)

"""This view updates an event. """
@api_view(['PUT'])
def eventUpdate(request, pk):
    event = Event.objects.get(id=pk)
    serializer = EventSerializer (instance=event, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
    

"""This view deletes an event. """
@api_view(['DELETE'])
def eventDelete (request, pk):
    event = Event.objects.get(id=pk) 
    event.delete()
    return Response ('Deleted')

# *** USER MANAGEMENT VIEWS ***

@api_view(['GET'])
def userGet(request, pk):
    """Retrieves a user's detail using primary key. Returns 404 if none."""
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['PUT'])
def userUpdate(request, pk):
    """Updates an existing user's detail. Returns 404 if user doesn't exist"""
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
