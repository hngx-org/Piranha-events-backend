from django.shortcuts import render
from rest_framework.response import Response

from .models import Event, Group
from .serializers import EventSerializer
from rest_framework import status

from .models import User, Event, Comment, InterestedEvent, User_group
from .serializers import CommentSerializer, ImageSerializer
from .serializers import GroupSerializer, User_groupSerializer

from .models import Image

from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def eventList(request):
    """This view returns a list of all events."""
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def eventDetail(request, pk):
    """This view returns the details of a specific event."""
    events = Event.objects.get(id=pk)
    serializer = EventSerializer(events, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def eventCreate(request):
    """This view creates a new event. """
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['PUT'])
def eventUpdate(request, pk):
    """This view updates an event. """
    event = Event.objects.get(id=pk)
    serializer = EventSerializer(instance=event, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def eventDelete(request, pk):
    """This view deletes an event. """
    event = Event.objects.get(id=pk)
    event.delete()
    return Response('Deleted')


@api_view(['POST'])
def express_interest(request, userId, eventId):
    user = get_object_or_404(User, pk=userId)
    event = get_object_or_404(Event, pk=eventId)

    # Check if the user is already interested in the event
    if InterestedEvent.objects.filter(user=user, event=event).exists():
        return Response(
            {"detail": "User is already interested in this event."},
            status=status.HTTP_400_BAD_REQUEST
            )

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
    interested_event = InterestedEvent.objects.filter(
        user=user, event=event).first()
    if not interested_event:
        return Response(
            {"detail": "User is not interested in this event."},
            status=status.HTTP_400_BAD_REQUEST
            )

    # Remove the interest
    interested_event.delete()

    # Respond with a success message
    return Response(
        {"detail": "Interest in the event has been removed."},
        status=status.HTTP_204_NO_CONTENT
        )


@api_view(['POST'])
def add_comment(request, eventId):
    """allows user to add a comment to an event"""

    try:
        event = Event.objects.get(pk=eventId)
    except Event.DoesNotExist:
        return Response(
            {'error': 'Event not found'},
            status=status.HTTP_404_NOT_FOUND
            )

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
        return Response(
            {'error': 'Event not found'},
            status=status.HTTP_404_NOT_FOUND
            )

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
        return Response({'error': 'Comment not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(comment=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_images_for_comment(request, commentId):
    """Gets images for a comment of an invent"""

    try:
        comment = Comment.objects.get(pk=commentId)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        images = Image.objects.filter(comment=comment)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

# new additions for Group


@api_view(['GET', 'POST'])
def groupListCreate(request):
    if request.method == 'GET':
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def groupDetail(request, pk):
    try:
        group = Group.objects.get(pk=pk)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GroupSerializer(group)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_goup(request):
    """creates a new group"""
    serializer = GroupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def get_groups(request):
    """gets all groups"""
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_specific_group(request, pk):
    """gets a specific group details"""
    groups = Group.objects.get(id=pk)
    serializer = GroupSerializer(groups, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def update_group(request, pk):
    """updates a group details"""
    group = Group.objects.get(id=pk)
    serializer = GroupSerializer(instance=group, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_group(request, pk):
    """deletes a group"""
    group = Group.objects.get(id=pk)
    group.delete()
    return Response('Deleted')
