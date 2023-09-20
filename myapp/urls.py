from django.urls import path 
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('events/', eventList, name='event-list'),
    path('events/<int:pk>/', eventDetail, name='event-detail'),
    path('events/create/', eventCreate, name='event-create'),
    path('events/<int:pk>/update/', eventUpdate, name='event-update'),
    path('events/<int:pk>/delete/', eventDelete, name='event-delete'),
]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)