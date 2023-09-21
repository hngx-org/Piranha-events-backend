from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.shortcuts import get_object_or_404

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


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


"""This view expresses interest of a user on an event"""
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


"""This view removes the interest of a user on an event"""
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


"""This View Allows For Users to add comments on an event"""
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


"""Fetches all Comments on an event"""
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


"""This View makes it possible for a user to add images when making comments"""
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


""" """
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


# New additions for Group
"""This view List all group or creates new group"""
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


"""view for comment likes"""
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def create_or_delete_comment_like(request, commentId):
    user = request.user

    try:
        # Retrieve the comment associated with the comment_pk
        comment = Comment.objects.get(id=commentId)
        
        # Check if a like already exists for this comment and user
        comment_like, created = CommentLike.objects.get_or_create(user=user, comment=comment)

        # If the like already exists and it's a DELETE request, delete it (undo the like)
        if request.method == 'DELETE':
            comment_like.delete()
            return Response({"message": "Comment unliked"}, status=status.HTTP_204_NO_CONTENT)

        # If it's a POST request and a new like is created, return a success response
        if created:
            # Serialize the comment_like object
            serializer = CommentLikeSerializer(comment_like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If a like already existed and it's a POST request, return a response indicating it's already liked
        return Response({"message": "Comment liked already"}, status=status.HTTP_400_BAD_REQUEST)

    except Comment.DoesNotExist:
        # Handle the case where the specified comment does not exist
        return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment_reply(request, commentId):
    user = request.user

    try:
        comment_reply = CommentReply(user=user, pk=commentId, **request.data)
        comment_reply.save()
        serializer = CommentReplySerializer(comment_reply)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except CommentReply.DoesNotExist:
        return Response({"message": "Comment does not exist"}, status=status.HTTP_404_NOT_FOUND)


"""This view makes it possible to Retrieve, Update and Delete a group"""
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


"""  """
@api_view(['POST'])
def create_goup(request):
    """creates a new group"""
    serializer = GroupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response (serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_groups(request):
    """gets all groups"""
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return Response (serializer.data)


"""  """
@api_view(['GET'])
def get_specific_group(request, pk):
    """gets a specific group details"""
    groups = Group.objects.get(id=pk)
    serializer = GroupSerializer(groups, many=False)
    return Response (serializer.data)


"""  """
@api_view(['PUT'])
def update_group(request, pk):
    """updates a group details"""
    group = Group.objects.get(id=pk)
    serializer = GroupSerializer (instance=group, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


"""  """
@api_view(['DELETE'])
def delete_group(request, pk):
    """deletes a group"""
    group = Group.objects.get(id=pk)
    group.delete()
    return Response ('Deleted')

# *** USER MANAGEMENT VIEWS ***

@api_view(['GET'])
def userGet(request, pk):
    """Retrieves a user's detail using primary key. Returns 404 if none."""
    user = get_object_or_404(User, pk=pk)

    if User.objects.filter(pk=pk).exists():
        serializer = UserSerializer(user)
        return Response(serializer.data)

    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def userUpdate(request, pk):
    """Updates an existing user's detail. Returns 404 if user doesn't exist"""
    user = get_object_or_404(User, pk=pk)

    if not User.objects.filter(pk=pk).exists():
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            
    return Response(serializer.data)