from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView
from rest_framework import status, permissions, viewsets, generics, serializers
from rest_framework.decorators import api_view, permission_classes
from .models import User, Group
from rest_framework import generics
from django.http import HttpRequest, HttpResponse
from rest_api_payload import error_response, success_response
from django.db.models import Count
from django.db.models import OuterRef, Subquery, F
from django.db.models.functions import Coalesce
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from social_django.utils import psa

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request





# from allauth.socialaccount.providers.base.views import SocialLoginView
# from allauth.socialaccount.providers.google.adapter import GoogleOAuth2Adapter
# from .serializers import GoogleLoginSerializer

# @api_view(['POST'])
# @permission_classes([AllowAny])
# @psa()
# def register_by_access_token(request, backend):
#     token = request.data.get('access_token')
#     user = request.backend.do_auth(token)
#     print(request)
#     if user:
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response(
#             {
#                 'token': token.key
#             },
#             status=status.HTTP_200_OK,
#             )
#     else:
#         return Response(
#             {
#                 'errors': {
#                     'token': 'Invalid token'
#                     }
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )


# @api_view(['GET', 'POST'])
# def authentication_test(request):
#     print(request.user)
#     return Response(
#         {
#             'message': "User successfully authenticated",
#             'id': request.user.id,
#             'name': request.user.name,
#             'email': request.user.email,
#             'avatar': request.user.avatar.url,
            
#         },
#         status=status.HTTP_200_OK,
#     )

class LoginView(APIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    # authentication_classes = [permissions.AllowAny]

    def post(self, request:HttpRequest):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            pass_id = serializer.validated_data["pass_id"]

            try:
                user = User.objects.get(email=email)
                token, created = Token.objects.get_or_create(user=user)
                payload = success_response(
                    status="success",
                    message="Login successful",
                    data={
                        "token": token.key,
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'avatar': user.avatar.url if user.avatar else None
                    }
                )
                return Response(data=payload, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                user = User.objects.create_user(email=email, password=pass_id)
                token, created = Token.objects.get_or_create(user=user)
                payload = success_response(
                    status="success",
                    message="Login successful",
                    data={
                        "token":token.key,
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'avatar': user.avatar.url if user.avatar else None
                    }
                )
                return Response(data=payload, status=status.HTTP_201_CREATED)
        else:
            payload = error_response(
                status="Failed, something went wrong", 
                message=serializer.errors
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class SingleGroupView(generics.ListAPIView):
    serializer_class = SinglePeopleGroupSerializer
    queryset = PeopleGroup.objects.all()
    
    def get(self, request:HttpRequest, id:int):
        try:

            group = PeopleGroup.objects.annotate(members_count=Count("members")).get(id=id)
            serializers = SinglePeopleGroupSerializer(instance=group)
            payload = success_response(
                status="success",
                message=f"{group.name} fetched successfully!",
                data=serializers.data
            )
            return Response(data=payload, status=status.HTTP_201_CREATED)
        except PeopleGroup.DoesNotExist:
            payload = error_response(
                status="Failed, something went wrong", 
                message=f"Group does not exist"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        

class GroupEventsView(generics.ListAPIView):
    serializer_class = GroupEventsSerializer

    def get(self, request:HttpRequest, id:int):
        try:
            group = PeopleGroup.objects.get(id=id)
            events = Event.objects.filter(group=group)
            serializers = GroupEventsSerializer(instance={'group': group, 'events': events}, many=False)
            payload = success_response(
                status="success",
                message=f"Events for group {group.name} fetched successfully!",
                data=serializers.data
            )
            return Response(data=payload, status=status.HTTP_200_OK)
        except PeopleGroup.DoesNotExist:
            payload = error_response(
                status="Failed, something went wrong", 
                message=f"Group does not exist"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

        
class AddUserGroupView(generics.CreateAPIView):
    serializer_class = AddUserToGroupSerializer
    queryset = PeopleGroup.objects.all()
    
    def post(self, request:HttpRequest):
        serializer = AddUserToGroupSerializer(data=request.data)

        if serializer.is_valid():
            user_id = serializer.validated_data["user_id"]
            group_id = serializer.validated_data["group_id"]
            
            try:
                group = PeopleGroup.objects.get(id=group_id)
            except PeopleGroup.DoesNotExist as e:
                # print(e)
                payload = error_response(
                    status="Failed, something went wrong",
                    message=f"{e}",
                )
                return Response(data=payload, status=status.HTTP_404_NOT_FOUND)
            
            
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist as e:
                # print(e)
                payload = error_response(
                    status="Failed, something went wrong",
                    message=f"{e}",
                )
                return Response(data=payload, status=status.HTTP_404_NOT_FOUND)
            # group = PeopleGroup.objects.get(id=group_id)
            # user = User.objects.get(id=user_id)
            
            group.user_set.add(user)
            group.members.add(user)
            
            payload = success_response(
                status="success",
                message=f"{user.name} has been added to {group.name}",
                data=serializer.data
            )
            return Response(data=payload, status=status.HTTP_201_CREATED)
                
                
        else:
            # print(serializer.errors)
            payload = error_response(
                status="Failed, something went wrong", 
                message=serializer.errors
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
class RemoveUserGroupView(generics.CreateAPIView):
    serializer_class = AddUserToGroupSerializer
    queryset = PeopleGroup.objects.all()
    
    def post(self, request:HttpRequest):
        serializer = AddUserToGroupSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data["user_id"]
            group_id = serializer.validated_data["group_id"]
            
            try:
                group = PeopleGroup.objects.get(id=group_id)
                user = User.objects.get(id=user_id)
                
                group.user_set.remove(user)
                group.members.remove(user)
                
                payload = success_response(
                    status="success",
                    message=f"{user.name} has been removed from {group.name}",
                    data=serializer.data
                )
                return Response(data=payload, status=status.HTTP_201_CREATED)
                
                
                
            except PeopleGroup.DoesNotExist or User.DoesNotExist:
                payload = error_response(
                    status="success",
                    message=f"Group or User does not exist",
                )
                return Response(data=payload, status=status.HTTP_404_NOT_FOUND)
        else:
            print(serializer.errors)
            payload = error_response(
                status="Failed, something went wrong", 
                message=serializer.errors
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
        
class CreateGroupView(generics.CreateAPIView):
    serializer_class = CreateGroupSerializer
    queryset = PeopleGroup.objects.all()
    
    def post(self, request:HttpRequest):
        serializer = None
        serializer = CreateGroupSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data["name"]
            user_id = serializer.validated_data["user"]
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist as e:
                payload = error_response(
                    status="failed", 
                    message=f"{e}"
                )
                return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            p_group = PeopleGroup.objects.get(name=name)
            p_group.user_set.add(user)
            p_group.members.add(user)
            p_group.save()
            payload = success_response(
                status="success",
                message=f"New Group ({name}) created successfully!",
                data=serializer.data
            )
            return Response(data=payload, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            payload = error_response(
                status="Failed, something went wrong", 
                message=serializer.errors
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class DeleteGroupView(generics.DestroyAPIView):
    serializer_class = PeopleGroupSerializer
    queryset = PeopleGroup.objects.all()
    
    def delete(self, request:HttpRequest, id:int):
        try:
            group = PeopleGroup.objects.get(id=id)
            group.delete()
            payload = success_response(
                status="success",
                message=f"{group.name} deleted successfully!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_201_CREATED)
        except PeopleGroup.DoesNotExist:
            payload = error_response(
                status="failed", 
                message=f"Group does not exist"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
class AllEventView(generics.ListAPIView):
    serializer_class = AllEventsSerializers
    queryset = Event.objects.all()
    
    def get(self, request:HttpRequest):
        try:
            event = self.get_queryset()
            serializers = AllEventsSerializers(event, many=True)
            payload = success_response(
                status="success",
                message=f"All events fetched successfully!",
                data=serializers.data
            )
            return Response(data=payload, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            payload = error_response(
                status="failed", 
                message=f"Group does not exist"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
class UserGroupView(generics.ListAPIView):
    serializer_class = UserPeopleGroupSerializer
    queryset = User.objects.all()
    
    def get_queryset(self, user):
        user_groups = PeopleGroup.objects.annotate(
            members_count=Count("members"),
            event_counts=Coalesce(Subquery(
                Event.objects.filter(group_id=OuterRef("pk"))
                .values("group")
                .annotate(count=Count("*"))
                .values("count")
            ), 0)
        ).filter(members=user)
        return user_groups
    
    def get(self, request:HttpRequest, id:int):
        try:
            serializer = None
            user = User.objects.get(id=id)
            
            user_groups = self.get_queryset(user)
            print(user_groups)
            serializers = UserPeopleGroupSerializer(user_groups, many=True)
            if user_groups.exists():
                
                payload = success_response(
                    status="success",
                    message=f"All groups for {user.name} fetched successfully!",
                    data=serializers.data
                )
                return Response(data=payload, status=status.HTTP_201_CREATED)
            else:
                payload = success_response(
                    status="success", 
                    message=f"User does not belong to any group",
                    data=serializers.data
                    
                )
                return Response(data=payload, status=status.HTTP_200_OK)
        except User.DoesNotExist or Exception as e :
            payload = error_response(
                status="failed", 
                message=f"{e}"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
class UserEventView(generics.ListAPIView):
    serializer_class = AllEventsSerializers
    queryset = Event.objects.all()
    
    def get(self, request:HttpRequest, id:int):
        try:
            user = User.objects.get(id=id)
            user_groups = PeopleGroup.objects.filter(members=user.id)
            if user_groups.exists():
                events = Event.objects.filter(group__in = [i.id for i in user_groups])
                serializers = AllEventsSerializers(events, many=True)
                payload = success_response(
                    status="success",
                    message=f"All events for {user.name} fetched successfully!",
                    data=serializers.data
                )
                return Response(data=payload, status=status.HTTP_201_CREATED)
            else:
                payload = success_response(
                    status="success", 
                    message=f"User does not belong to any group",
                    data=serializers.data
                    
                )
                return Response(data=payload, status=status.HTTP_200_OK)
        except User.DoesNotExist or Exception as e :
            payload = error_response(
                status="failed", 
                message=f"{e}"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
class SingleEventView(generics.ListAPIView):
    serializer_class = EventsSerializers
    queryset = Event.objects.all()
    
    def get(self, request:HttpRequest, id:int):
        try:
            event = Event.objects.get(id=id)
            serializers = EventsSerializers(event)
            payload = success_response(
                    status="success", 
                    message=f"Event retrieved",
                    data=serializers.data
                    
            )
            return Response(data=payload, status=status.HTTP_200_OK)
                
        except Event.DoesNotExist or Exception as e :
            payload = error_response(
                status="failed", 
                message=f"{e}"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
              
class CreateEventView(generics.CreateAPIView):
    serializer_class = CreateEventSerializer
    queryset = Event.objects.all()
    
    def post(self, request:HttpRequest):
        serializer = CreateEventSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data["title"]
            description = serializer.validated_data["description"]
            location = serializer.validated_data["location"]
            start_time = serializer.validated_data["start_time"]
            end_time = serializer.validated_data["end_time"]
            group = serializer.validated_data["group"]
            owner = serializer.validated_data["owner"]
            thumbnail = serializer.validated_data["thumbnail"]

            user = User.objects.get(id=owner)
            people_group = PeopleGroup.objects.get(id=group)
            try:
                Event.objects.create(title=title, description=description, location=location, start_time=start_time, end_time=end_time, group=people_group, owner=user, thumbnail=thumbnail)
                payload = success_response(
                    status="success",
                    message=f"New Event ({title}) created successfully!",
                    data=serializer.data
                )
            except Exception as e:
                payload = error_response(
                    status="success",
                    message=f"{e}",
                )
            return Response(data=payload, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            payload = error_response(
                status="Failed, something went wrong", 
                message=serializer.errors
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

class CreateEventCommentView(generics.CreateAPIView):
    serializer_class = CreateCommentSerializer
    queryset = Comment.objects.all()



    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request:HttpRequest):
        serializer = CreateCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            payload = success_response(
                    status="success",
                    message=f"Comment added successfully!",
                    data=serializer.data
                )
            return Response(data=payload, status=status.HTTP_201_CREATED)
        else:
            payload = error_response(
                status="Failed something went wrong",
                message=serializer.errors
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

class EventCommentListView(generics.ListAPIView):
    queryset =  Comment.objects.all()
    def get(self, request:HttpRequest, event_id):
        try:
            comments = Comment.objects.filter(event_id=event_id)
            serializers = CommentSerializer(comments, many=True)
            payload = success_response(
                status="success",
                message=f"All comments for event {event_id} fetched successfully!",
                data=serializers.data
            )
            return Response(data=payload, status=status.HTTP_200_OK)
        except Exception as e:
            payload = error_response(
                status="failed", 
                message=f"Event does not exist"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)

class LikeView(generics.CreateAPIView):
    serializer_class = LikeSerializers
    queryset = Likes.objects.all()
    def post(self, request:HttpRequest):
        serializer = LikeSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            payload = success_response(
                    status="success",
                    message=f"Comment liked successfully!",
                    data=serializer.data
                )
            return Response(data=payload, status=status.HTTP_201_CREATED)
        else:
            # print(serializer.errors)
            payload = error_response(
                status="Failed, something went wrong", 
                message=serializer.errors
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteLikeView(generics.DestroyAPIView):
    serializer_class = LikeSerializers
    queryset = Likes.objects.all()
    
    def delete(self, request:HttpRequest, id:int):
        try:
            like = Likes.objects.get(id=id)
            like.delete()
            payload = success_response(
                status="success",
                message=f"Like removed",
                data={}
            )
            return Response(data=payload, status=status.HTTP_201_CREATED)
        except Likes.DoesNotExist:
            payload = error_response(
                status="failed", 
                message=f"Like does not exist"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
class InterestEventView(generics.CreateAPIView):
    serializer_class = InterestedUserEventSerializers
    queryset = InterestedEvent.objects.all()
    def post(self, request:HttpRequest):
        serializer = InterestedUserEventSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            payload = success_response(
                    status="success",
                    message=f"Interest has been shown in event",
                    data=serializer.data
                )
            return Response(data=payload, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            payload = error_response(
                status="Failed, something went wrong", 
                message=serializer.errors
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
        
class InterestDeleteEventView(generics.DestroyAPIView):
    serializer_class = InterestedUserEventSerializers
    queryset = Likes.objects.all()
    
    def delete(self, request:HttpRequest, id:int):
        try:
            i_event = InterestedEvent.objects.get(id=id)
            i_event.delete()
            payload = success_response(
                status="success",
                message=f"Interest in event revoked",
                data={}
            )
            return Response(data=payload, status=status.HTTP_201_CREATED)
        except Likes.DoesNotExist:
            payload = error_response(
                status="failed", 
                message=f"Interest does not exist"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
class EventInterestUserView(generics.ListAPIView):
    serializer_class = InterestedUserEventSerializers
    queryset = InterestedEvent.objects.all()
    
    def get(self, request:HttpRequest, id:int):
        try:
            event = InterestedEvent.objects.filter(event_id=id)
            serializers = InterestedUserEventSerializers(event, many=True)
            payload = success_response(
                    status="success", 
                    message=f"Interested users retrieved",
                    data=serializers.data
                    
            )
            return Response(data=payload, status=status.HTTP_200_OK)
                
        except Event.DoesNotExist or Exception as e :
            payload = error_response(
                status="failed", 
                message=f"{e}"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        

class AcceptInterestEventView(generics.CreateAPIView):
    serializer_class = InterestedUserEventSerializers
    queryset = InterestedEvent.objects.all()
    def post(self, request:HttpRequest, id:int):
        try:
            i_event = InterestedEvent.objects.get(id=id)
            user = User.objects.get(id=i_event.user_id.id)
            event = Event.objects.get(id=i_event.event_id.id)
            group = PeopleGroup.objects.get(id=event.group.id)
            
            group.user_set.add(user)
            group.members.add(user)
            i_event.delete()
            
            payload = success_response(
                    status="success",
                    message=f"{user.name} has been invited to {group.name}",
                    data={}
                )
            return Response(data=payload, status=status.HTTP_201_CREATED)
            
        except InterestedEvent.DoesNotExist as e:
            payload = error_response(
                status="Failed", 
                message=f"{e}"
            )
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)


class LogoutSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

#class LogoutView(generics.CreateAPIView):
#    serializer_class = LogoutSerializer

#    def create(self, request, *args, **kwargs):
#        try:
#            user_id = self.request.data.get('user_id')
#            user = User.objects.get(id=user_id)
#            try:
#                token = Token.objects.get(user=user)
#                token.delete()
#                return Response({'message': 'User successfully logged out.'}, status=status.HTTP_200_OK)
#            except Token.DoesNotExist:
#                return Response({'error': 'Token does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
#        except User.DoesNotExist:
#            return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.CreateAPIView):
    serializer_class = LogoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user_id')
            try:
                user = User.objects.get(id=user_id)
                try:
                    token = Token.objects.get(user=user)
                    token.delete()
                    return Response({'message': 'User successfully logged out.'}, status=status.HTTP_200_OK)
                except Token.DoesNotExist:
                    return Response({'error': 'Token does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)