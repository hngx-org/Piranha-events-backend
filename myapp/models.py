from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
from myapp.custom_user_manager import CustomUserManager
# Create your models here.



class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=250, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'user'

# Images Model
class Image(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.ImageField()

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'images'


class Event(models.Model):
    """Model representing an event."""
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=1024)
    location = models.CharField(max_length=1024)
    creator_id = models.ForeignKey('User', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


    class Meta:
        verbose_name ='Event'
        verbose_name_plural = 'Events'
        db_table = 'events'

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
# class EventThumbnail(models.Model):
#     image_id()
#     event_id()
#     class Meta:
#         db_table = 'event_thumbnail'

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    body = models.TextField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.ForeignKey("Event", on_delete=models.DO_NOTHING)
    
    class Meta:
        db_table = 'comments'
        
    def __str__(self):
        return self.body
    
# class CommentImages(models.Model):
#     comment_id()
#     image_id()
    
#     class Meta:
#         db_table = 'comment_images'
        
        
class Group(models.Model):
    """model for group resource"""
    title = models.CharField(max_length=255)

    class Meta:
        db_table = 'groups'
        
    def __str__(self):
        return self.title
    

class UserGroup(models.Model):
    """model for the user group object"""
    user_id= models.ForeignKey("User",on_delete=models.DO_NOTHING)
    group_id= models.ForeignKey("Group", on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.group_id
    
    class Meta:
        db_table = 'user_groups_table'


# class GroupEvent(models.Model):
#     group_id()
#     event_id()
    
#     def __str__(self):
#         return self.group_id
    
#     class Meta:
#         db_table = 'group_events'
        
        
# class GroupImage(models.Model):
#     group_id()
#     image_id()
    
#     class Meta:
#         db_table = 'group_image'
        
#     def __str__(self):
#         return self.group_id
    
# Interested Events Model
class InterestedEvent(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    event_id = models.ForeignKey("Event", on_delete=models.CASCADE)

    def __str__(self):
        return self.event_id
    class Meta:
        db_table = 'interested_events'
        
        
# class Likes(models.Model):
#     user_id()
#     comment_id()
    
#     def __str__(self):
#         return self.comment_id
#     class Meta:
#         db_table = 'likes'

