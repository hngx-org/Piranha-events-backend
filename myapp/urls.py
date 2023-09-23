from django.urls import path,include, re_path
from .views import *
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'events', EventViewSet)


urlpatterns = [
    # google auth 
    # re_path('register-by-access-token/' + r'social/(?P<backend>[^/]+)/$', register_by_access_token),
    # path('authentication-test/', authentication_test),
    # path('social-auth/google-oauth2/', register_by_access_token),
    # path('', include('social_django.urls', namespace='social')),
    
    
    path('login/', LoginView.as_view(), name='login-group'),
    path('logout/', LogoutView.as_view(), name='logout'),

    
    path('group/', CreateGroupView.as_view(), name='create-group'),
    path('group/add_user/', AddUserGroupView.as_view(), name='adduser-group'),
    path('group/remove_user/', RemoveUserGroupView.as_view(), name='removeuser-group'),
    path('group/<int:id>/', DeleteGroupView.as_view(), name='delete-group'),
    path('group/<int:id>/', SingleGroupView.as_view(), name='single-group'),
    path('group/user/<int:id>/', UserGroupView.as_view(), name='user-group'),
    
    path('group/<int:id>/events/', GroupEventsView.as_view(), name = 'list-group-events'),
    
    
    path('event/', CreateEventView.as_view(), name='create-event'),
    path('events/', AllEventView.as_view(), name='all-event'),
    path('event/<int:id>/', SingleEventView.as_view(), name='single-event'),
    path('event/user/<int:id>/', UserEventView.as_view(), name='user-events'),
    
    
    
    path('comment/', CreateEventCommentView.as_view(), name='create-comment'),
    path('comment/list/<int:event_id>/', EventCommentListView.as_view(), name='list-comment'),
    path('like/', LikeView.as_view(), name='like-comment'),
    path('like/<int:id>/', DeleteLikeView.as_view(), name='like-comment'),
    
    
    path('interested_event/', InterestEventView.as_view(), name='i_event'),
    path('interested_event/<int:id>/', InterestDeleteEventView.as_view(), name='i_event-delete'),
    path('interested_event/event/<int:id>/', EventInterestUserView.as_view(), name='i_event-interests'),
    path('interested_event/accept/<int:id>/', AcceptInterestEventView.as_view(), name='i_event-accept-interests'),
    
    
    # path('users/<int:pk>', userGet, name='user-get'),
    # path('users/<int:pk>/update', userUpdate, name='user-update'),


    # # Event Management
    # path('', include(router.urls)),
    
    
    # path('api/events/comments/', add_comment, name='add-comment'),
    # # path('events/<int:eventId>/comments/', add_comment, name='add-comment'),
    # path('events/<int:eventId>/comments/', get_comments, name='get-comments'),

    # # image
    # path('images/', ImageListCreateView.as_view(), name='image-list-create'),
    # path('images/<int:pk>/', ImageDetailView.as_view(), name='image-detail'),
  
    # path('comments/<int:commentId>/images/', add_image_to_comment, name='add-image-to-comment'),
    # path('comments/<int:commentId>/images/', get_images_for_comment, name='get-images-for-comment'),

    # # Express interest in an event
    # path('users/<int:userId>/interests/<int:eventId>/', express_interest, name='express-interest'),
    # # Remove interest in an event
    # path('users/<int:userId>/interests/<int:eventId>/', remove_interest, name='remove-interest'),

    # path('groups/',create_goup, name='group-create'),
    # path('groups/<int:pk>/', get_specific_group, name='group-detail'),
    # path('groups/<int:pk>/', update_group, name='group-update'),
    # path('groups/<int:pk>/', delete_group, name='group-delete'),
    # path('groups/', get_groups, name='group-list'),


    
    # path('groups/<int:groupId>/members/<int:userId>', add_user_to_group, name='group-user-create'),
    # path('groups/<int:groupId>/members/<int:userId>', remove_user_from_group, name='group-user-delete'),
    # path('groups/<int:groupId>/members/', group_members_list, name='group-members-list'),

    # path('comments/<int:commentId>/likes/', add_likes_to_comment, name='add-likes-to-comment'),
    # path('comments/<int:commentId>/likes/', get_likes_for_comment, name='get-likes-for-comment'),
    # path('comments/<int:commentId>/likes/', delete_likes_for_comment, name='delete-likes-for-comment'),
]

