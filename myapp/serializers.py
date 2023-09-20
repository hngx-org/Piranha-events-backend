from rest_framework import serializers
from . models import Event, InterestedEvent

class EventSerializer(serializers.ModelSerializer):
    """EventSerializer class converts Event objects to and from JSON."""
    class Meta:
        model = Event
        fields = '__all__'

class InterestedEventSerializer(serializers.ModelSerializer):
    """
    serialise InterestedEvent to and from JSON
    """
    class Meta:
        model = InterestedEvent
        fields = '__all__'
