from django.shortcuts import render
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer
from rest_framework import status
from .models import User, Event, Comment, InterestedEvent
#from .serializers import CommentSerializer, ImageSerializer
from .models import Image
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

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


@api_view(['POST'])
def express_interest(request, userId, eventId):
    user = get_object_or_404(User, pk=userId)
    event = get_object_or_404(Event, pk=eventId)

    # Check if the user is already interested in the event
    if InterestedEvent.objects.filter(user=user, event=event).exists():
        return Response({"detail": "User is already interested in this event."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new InterestedEvent
    interested_event = InterestedEvent(user=user, event=event)
    interested_event.save()

    # Serialize the created InterestedEvent and return it in the response
    serializer = InterestedEventSerializer(interested_event)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def remove_interest(request, userId, eventId):
    user = get_object_or_404(User, pk=userId)
    event = get_object_or_404(Event, pk=eventId)

    # Check if the user is interested in the event
    interested_event = InterestedEvent.objects.filter(user=user, event=event).first()
    if not interested_event:
        return Response({"detail": "User is not interested in this event."}, status=status.HTTP_400_BAD_REQUEST)

    # Remove the interest
    interested_event.delete()

    # Respond with a success message
    return Response({"detail": "Interest in the event has been removed."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def add_comment(request, eventId):
    """allows user to add a comment to an event"""

    try:
        event = Event.objects.get(pk=eventId)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_comments(request, eventId):
    """Gets comments for an event"""
    try:
        event = Event.objects.get(pk=eventId)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        comments = Comment.objects.filter(event=event)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def add_image_to_comment(request, commentId):
    """adds an image to a comment"""

    try:
        comment = Comment.objects.get(pk=commentId)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(comment=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_images_for_comment(request, commentId):
    """Gets images for a comment"""

    try:
        comment = Comment.objects.get(pk=commentId)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        images = Image.objects.filter(comment=comment)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)





