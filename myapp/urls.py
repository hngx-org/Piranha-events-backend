from django.urls import path 
from .views import *

urlpatterns = [
    # User Management
    # Event Management
    path('events/', eventList, name='event-list'),
    path('events/<int:pk>/', eventDetail, name='event-detail'),
    path('events/create/', eventCreate, name='event-create'),
    path('events/<int:pk>/update/', eventUpdate, name='event-update'),
    path('events/<int:pk>/delete/', eventDelete, name='event-delete'),
    path('api/events/<int:eventId>/comments/', add_comment, name='add-comment'),
    path('api/events/<int:eventId>/comments/', get_comments, name='get-comments'),
    path('api/comments/<int:commentId>/images/', add_image_to_comment, name='add-image-to-comment'),
    path('api/comments/<int:commentId>/images/', get_images_for_comment, name='get-images-for-comment'),

    # User Interaction
    path('api/groups/', views.groupListCreate, name='group-list-create'),
    path('api/groups/<int:pk>/', views.groupDetail, name='group-detail'),
]
