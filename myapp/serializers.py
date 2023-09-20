from rest_framework import serializers
from . models import Event, Comment

class EventSerializer(serializers.ModelSerializer):
    """EventSerializer class converts Event objects to and from JSON."""
    class Meta:
        model = Event
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    """This is a class serilializer, it converts comment objects to and from json"""
    class Meta:
        model = Comment
        fields = '__all__'
