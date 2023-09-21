from rest_framework import serializers
from django.core import validators
from .models import Group

import base64


from .models import *

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
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    """GroupSerializer class converts Group objects to and from JSON."""

    class Meta:
        model = Group
        fields = "__all__"
    
    title = models.CharField(max_length=255)

    # Add validation for the title field
    def validate_title(self, value):
        if not value.strip():  # Check if the title is empty or contains only whitespace
            raise serializers.ValidationError("Title cannot be empty or contain only whitespace.")
        return value

class UserGroupSerializer(serializers.ModelSerializer):
    """User_groupSerializer class converts User_group objects to and from JSON."""

    class Meta:
        model = UserGroup
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """This is a class serilializer, it converts comment objects to and from json"""

    class Meta:
        model = Comment
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    """This serializer transforms Image objects to json and back to binary"""

    image_data = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = "__all__"

    def get_image_data(self, obj):
        with obj.image_field.open() as img_file:
            img_data = base64.b64encode(img_file.read()).decode("utf-8")
        return img_data

class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""
    class Meta:
        model = User
        fields = '__all__'
