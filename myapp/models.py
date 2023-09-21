from tabnanny import verbose
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email address must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=250, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'user'

# Images Model
class Image(models.Model):
    url = models.ImageField()#this should be a url field or something

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
    
class EventThumbnail(models.Model):
    image_id = models.ForeignKey(Image, on_delete=models.DO_NOTHING)
    event_id = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    class Meta:
        db_table = 'event_thumbnail'

class Comment(models.Model):
    body = models.TextField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.ForeignKey("Event", on_delete=models.DO_NOTHING)
    
    class Meta:
        db_table = 'comments'
        
    def __str__(self):
        return self.body
    
class CommentImages(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.DO_NOTHING)
    image_id = models.ForeignKey(Image, on_delete=models.DO_NOTHING)   
    class Meta:
        db_table = 'comment_images'
        
        
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
        db_table = 'user_group'



class GroupEvent(models.Model):
    group_id = models.ForeignKey("Group", on_delete=models.CASCADE)
    event_id = models.ForeignKey("Event", on_delete=models.CASCADE)

    def __str__(self):
        return self.group_id

    class Meta:
        db_table = 'group_events'


class GroupImage(models.Model):
    group_id = models.ForeignKey("Group", on_delete=models.CASCADE)
    image_id = models.ForeignKey("Image", on_delete=models.CASCADE)

    class Meta:
        db_table = 'group_image'

    def __str__(self):
        return self.group_id

    
# Interested Events Model
class InterestedEvent(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    event_id = models.ForeignKey("Event", on_delete=models.CASCADE)

    def __str__(self):
        return self.event_id
    class Meta:
        db_table = 'interested_events'


class Likes(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    comment_id = models.ForeignKey("Comment", on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_id

    class Meta:
        db_table = 'likes'
