from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import status, permissions, viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from .models import User, Group


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    # to modify the DELETE request to return a response when deleting a specific event by ID
    @action(detail=True, methods=['DELETE'])
    def delete_event(self, request, pk=None):
        """Deletes an event by ID"""

        try:
            event = self.get_object()
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        event.delete()  # Delete the event
        return Response({'message': 'Event deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


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
def add_comment(request):
    """Allows a user to add a comment to an event"""

    event_id = request.data.get('eventId')  # Get event ID from request data

    try:
        event = Event.objects.get(pk=event_id)
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
    
# to add image,update, delete and to view
class ImageListCreateView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

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

# @api_view(['POST'])
# def create_goup(request):
#     """creates a new group"""
#     serializer = GroupSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response (serializer.data)

@api_view(['POST'])
def create_group(request):
    """creates a new group"""

    serializer = GroupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
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



@api_view(['POST'])
def add_user_to_group(request, groupId, userId):
    try:
        group = Group.objects.get(id=groupId)
        user = User.objects.get(id=userId)
        group.user_set.add(user)
        return Response(status=status.HTTP_201_CREATED)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def remove_user_from_group(request, groupId, userId):
    try:
        group = Group.objects.get(id=groupId)
        user = User.objects.get(id=userId)
        group.user_set.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def group_members_list(request, groupId):
    try:
        group = Group.objects.get(id=groupId)
        members = group.user_set.all()
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    

@api_view(['POST'])
def add_likes_to_comment(request, commentId):
    if request.method == 'POST':
        serializer = LikesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_likes_for_comment(request, commentId):
    if request.method == 'GET':
        likes = Likes.objects.filter(comment_id=commentId)
        serializer = LikesSerializer(likes, many=True)
        return Response(serializer.data)

@api_view(['DELETE'])
def delete_likes_for_comment(request, commentId):
    if request.method == 'DELETE':
        likes = Likes.objects.filter(comment_id=commentId)
        likes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

