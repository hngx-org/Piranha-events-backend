from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, GoogleLoginView

router = DefaultRouter()
router.register(r'events', EventViewSet)


urlpatterns = [
    # google auth 
    path('auth/', GoogleLoginView.as_view(), name='google-login'), # full url path: api/accounts/auth
    
    path('users/<int:pk>/', userGet, name='user-get'),
    path('users/<int:pk>/update', userUpdate, name='user-update'),

    # Event Management
    path('', include(router.urls)),
    
    
    path('api/events/comments/', add_comment, name='add-comment'),
    # path('events/<int:eventId>/comments/', add_comment, name='add-comment'),
    path('events/<int:eventId>/comments/', get_comments, name='get-comments'),

    # image
    path('images/', ImageListCreateView.as_view(), name='image-list-create'),
    path('images/<int:pk>/', ImageDetailView.as_view(), name='image-detail'),
  
    path('comments/<int:commentId>/images/', add_image_to_comment, name='add-image-to-comment'),
    path('comments/<int:commentId>/images/', get_images_for_comment, name='get-images-for-comment'),

    # Express interest in an event
    path('users/<int:userId>/interests/<int:eventId>/', express_interest, name='express-interest'),
    # Remove interest in an event
    path('users/<int:userId>/interests/<int:eventId>/', remove_interest, name='remove-interest'),

    path('groups/',create_group, name='group-create'),
    path('groups/<int:pk>/', get_specific_group, name='group-detail'),
    path('groups/<int:pk>/', update_group, name='group-update'),
    path('groups/<int:pk>/', delete_group, name='group-delete'),
    path('groups/', get_groups, name='group-list'),

    
    path('groups/<int:groupId>/members/<int:userId>', add_user_to_group, name='group-user-create'),
    path('groups/<int:groupId>/members/<int:userId>', remove_user_from_group, name='group-user-delete'),
    path('groups/<int:groupId>/members/', group_members_list, name='group-members-list'),

    path('comments/<int:commentId>/likes/', add_likes_to_comment, name='add-likes-to-comment'),
    path('comments/<int:commentId>/likes/', get_likes_for_comment, name='get-likes-for-comment'),
    path('comments/<int:commentId>/likes/', delete_likes_for_comment, name='delete-likes-for-comment'),
]

