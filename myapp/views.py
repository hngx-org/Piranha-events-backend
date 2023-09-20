from django.shortcuts import render
from rest_framework.response import Response
from .models import Event,Group,User_group
from .serializers import EventSerializer
from rest_framework import status
from .models import Event, Comment
#from .serializers import CommentSerializer, ImageSerializer
from .serializers import GroupSerializer, User_groupSerializer
from .models import Image
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
    """Gets images for a comment of an invent"""

    try:
        comment = Comment.objects.get(pk=commentId)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        images = Image.objects.filter(comment=comment)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def create_goup(request):
    """creates a new group"""
    serializer = GroupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response (serializer.data)


@api_view(['GET'])
def get_groups(request):
    """gets all groups"""
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return Response (serializer.data)


@api_view(['GET'])
def get_specific_group(request, pk):
    """gets a specific group details"""
    groups = Group.objects.get(id=pk)
    serializer = GroupSerializer(groups, many=False)
    return Response (serializer.data)


@api_view(['PUT'])
def update_group(request, pk):
    """updates a group details"""
    group = Group.objects.get(id=pk)
    serializer = GroupSerializer (instance=group, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_group(request, pk):
    """deletes a group"""
    group = Group.objects.get(id=pk)
    group.delete()
    return Response ('Deleted')
