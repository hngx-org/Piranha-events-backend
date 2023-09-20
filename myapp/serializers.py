from rest_framework import serializers
from . models import Event, Group

class EventSerializer(serializers.ModelSerializer):
    """EventSerializer class converts Event objects to and from JSON."""
    class Meta:
        model = Event
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
