from rest_framework import serializers
from django.core import validators
# from .models import Group
from django.db.models import OuterRef, Subquery, F, Count
from django.db.models.functions import Coalesce

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

# class UserGroupSerializer(serializers.ModelSerializer):
#     """User_groupSerializer class converts User_group objects to and from JSON."""

#     class Meta:
#         model = UserGroup
#         fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """This is a class serilializer, it converts comment objects to and from json"""

    class Meta:
        model = Comment
        fields = "__all__"


# class ImageSerializer(serializers.ModelSerializer):
#     """This serializer transforms Image objects to json and back to binary"""

#     image_data = serializers.SerializerMethodField()

#     class Meta:
#         model = Image
#         fields = "__all__"

    def get_image_data(self, obj):
        with obj.image_field.open() as img_file:
            img_data = base64.b64encode(img_file.read()).decode("utf-8")
        return img_data

class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""
    class Meta:
        model = User
        fields = '__all__'

class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['user_id', 'comment_id']
        
        
        
class PeopleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleGroup
        fields = ['name', 'image']
        
class CreateGroupSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField()
    class Meta:
        model = PeopleGroup
        fields = ['name', 'image', 'user']
        
class SinglePeopleGroupSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField()
    events = serializers.SerializerMethodField()
    class Meta:
        model = PeopleGroup
        fields = '__all__'
        
        
    def get_events(self, obj):
        events = Event.objects.annotate(
            comment_counts=Coalesce(Subquery(
                Comment.objects.filter(event_id=OuterRef("pk"))
                .values("event")
                .annotate(count=Count("*"))
                .values("count")
            ), 0)
            
            ).filter(group__name=obj.name)
        serializer = AllEventsWithCommentsSerializers(events, many=True)
        return serializer.data
        
class UserPeopleGroupSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField()
    event_counts = serializers.IntegerField()
    class Meta:
        model = PeopleGroup
        fields ='__all__' #['name', 'image', 'members_count', 'event_counts']
        
class AddUserToGroupSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    group_id = serializers.IntegerField()

class AllEventsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        
    def to_representation(self, instance):
        rep = super(AllEventsSerializers, self).to_representation(instance)
        rep['owner'] = instance.owner.name
        rep['group'] = instance.group.name
        return rep
    
    
class AllEventsWithCommentsSerializers(serializers.ModelSerializer):
    comment_counts = serializers.IntegerField()
    class Meta:
        model = Event
        fields = '__all__'
        
        
    def to_representation(self, instance):
        rep = super(AllEventsWithCommentsSerializers, self).to_representation(instance)
        rep['owner'] = instance.owner.name
        rep['group'] = instance.group.name
        return rep

class CreateEventSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    location = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    owner = serializers.IntegerField()
    group = serializers.IntegerField()
    thumbnail = serializers.ImageField()
    
    
class CommentImageSerializers(serializers.ModelSerializer):
    
    
    class Meta:
        model = CommentImages
        fields = '__all__'
    
class CreateCommentSerializer(serializers.ModelSerializer):
    images = CommentImageSerializers(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.FileField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only = True
    )
    class Meta:
        model = Comment
        fields = ['id', 'body', 'user', 'event', 'images', 'uploaded_images']
        
    def validate(self, attrs):
        # attrs['user'] = User.objects.get(id=attrs['user']).id
        # attrs['event'] = Event.objects.get(id=attrs['event'])
        return attrs
    
    
    def create(self, validated_data):
        uploaded_data = validated_data.pop('uploaded_images')
        comment = Comment.objects.create(**validated_data)
        for i in uploaded_data:
            CommentImages.objects.create(comment_id = comment, image = i)
        return comment
class CommentImageOnlySerializers(serializers.ModelSerializer):
    class Meta:
        model = CommentImages
        fields = ['image']
class SingleEventCommentSerializers(serializers.ModelSerializer):
    comment_images = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'
        
    def get_comment_images(self, obj):
        comment_images = CommentImages.objects.filter(comment_id=obj.id)
        serializer = CommentImageOnlySerializers(comment_images, many=True)
        return serializer.data

class EventsSerializers(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = '__all__'

    def get_comments(self, obj):
        comments = Comment.objects.filter(event__id=obj.id)
        serializer = SingleEventCommentSerializers(comments, many=True)
        return serializer.data
    
    def get_user_info(self, obj):
        print(obj)
        user = User.objects.get(id=obj.owner.id)
        return {
            'id' : user.id,
            'name' : user.name,
            'image' : user.avatar.url if user.avatar else user.avatar,
        }
        
class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'
        
class InterestedUserEventSerializers(serializers.ModelSerializer):
    class Meta:
        model = InterestedEvent
        fields = '__all__'
        


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    pass_id = serializers.CharField()
    
class GroupEventsSerializer(serializers.Serializer):
    group = SinglePeopleGroupSerializer()
    events = EventsSerializers(many=True)
