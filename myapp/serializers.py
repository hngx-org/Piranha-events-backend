from rest_framework import serializers
from . models import Event, Group, User_group

class EventSerializer(serializers.ModelSerializer):
    """EventSerializer class converts Event objects to and from JSON."""
    class Meta:
        model = Event
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    """GroupSerializer class converts Group objects to and from JSON."""
    class Meta:
        model = Group
        fields = '__all__'

class User_groupSerializer(serializers.ModelSerializer):
    """User_groupSerializer class converts User_group objects to and from JSON."""
    class Meta:
        model = User_group
        fields = '__all__'