from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from .views import EventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)


urlpatterns = [
    
    # Event Management
    path('', include(router.urls)),
  
    path('events/<int:eventId>/comments/', add_comment, name='add-comment'),
    path('events/<int:eventId>/comments/', get_comments, name='get-comments'),
  
    path('comments/<int:commentId>/images/', add_image_to_comment, name='add-image-to-comment'),
    path('api/comments/<int:commentId>/images/', get_images_for_comment, name='get-images-for-comment'),

    # Express interest in an event
    path('users/<int:userId>/interests/<int:eventId>/', express_interest, name='express-interest'),
    # Remove interest in an event
    path('users/<int:userId>/interests/<int:eventId>/', remove_interest, name='remove-interest'),

    path('groups/', get_groups, name='group-list'),
    path('groups/create',create_goup, name='group-create'),
    path('groups/<int:groupId>', get_specific_group, name='group-detail'),
    path('groups/<int:groupId>/update', update_group, name='group-update'),
    path('groups/<int:groupId>/delete', delete_group, name='group-delete'),

]
