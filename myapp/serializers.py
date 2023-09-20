from rest_framework import serializers
from . models import Event, User

class EventSerializer(serializers.ModelSerializer):
    """EventSerializer class converts Event objects to and from JSON."""
    class Meta:
        model = Event
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""
    class Meta:
        model = User
        fields = '__all__'
