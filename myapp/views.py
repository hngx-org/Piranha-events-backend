from django.shortcuts import render
from rest_framework. response import Response 
from .models import Event
from .serializers import EventSerializer
from rest_framework.decorators import api_view


from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter



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