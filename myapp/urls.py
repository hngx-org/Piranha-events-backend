from django.urls import path 
from .views import *

urlpatterns = [
    
    # Event Management
    path('events/', eventList, name='event-list'),
    path('events/<int:pk>/', eventDetail, name='event-detail'),
    path('events/create/', eventCreate, name='event-create'),
    path('events/<int:pk>/update/', eventUpdate, name='event-update'),
    path('events/<int:pk>/delete/', eventDelete, name='event-delete'),
  
    path('events/<int:eventId>/comments/', add_comment, name='add-comment'),
    path('events/<int:eventId>/comments/', get_comments, name='get-comments'),
  
    path('comments/<int:commentId>/images/', add_image_to_comment, name='add-image-to-comment'),
    path('comments/<int:commentId>/images/', get_images_for_comment, name='get-images-for-comment'),
    # URL for comment likes
    path('comments/<int:commentId>/like/', create_or_delete_comment_like, name='create_or_delete_comment_like'),
    # URL for creating CommentReply
    path('comments/<int:commentId>/reply/', create_comment_reply, name='create_comment_reply'),

    # Express interest in an event
    path('users/<int:userId>/interests/<int:eventId>/', express_interest, name='express-interest'),
    # Remove interest in an event
    path('users/<int:userId>/interests/<int:eventId>/', remove_interest, name='remove-interest'),

    path('groups/', get_groups, name='group-list'),
    path('groups/create/',create_goup, name='group-create'),
    path('groups/<int:groupId>/', get_specific_group, name='group-detail'),
    path('groups/<int:groupId>/update/', update_group, name='group-update'),
    path('groups/<int:groupId>/delete/', delete_group, name='group-delete'),

]
