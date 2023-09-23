from tabnanny import verbose
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
import uuid

# Create your models here.
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email address must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.name = uuid.uuid4()
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


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    name = models.CharField(max_length=250, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(default='profile.jpg')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()


    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'



class Event(TimestampedModel):
    """Model representing an event."""
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=1024)
    location = models.CharField(max_length=1024)
    owner = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey("PeopleGroup", on_delete=models.CASCADE)
    thumbnail = models.ImageField(("Event Image"))
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


    class Meta:
        verbose_name ='Event'
        verbose_name_plural = 'Events'
        db_table = 'events'

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Comment(TimestampedModel):
    body = models.TextField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.ForeignKey("Event", on_delete=models.DO_NOTHING)
    
    
    class Meta:
        db_table = 'comments'

    def __str__(self):
        return self.body

class CommentImages(TimestampedModel):
    comment_id = models.ForeignKey(Comment, on_delete=models.DO_NOTHING)
    image = models.ImageField()
    class Meta:
        db_table = 'comment_images'


# class Group(TimestampedModel):
#     """model for group resource"""
#     title = models.CharField(max_length=255)

#     class Meta:
#         db_table = 'groups'
        
#     def __str__(self):
#         return self.title
    

# class UserGroup(TimestampedModel):
#     """model for the user group object"""
#     user_id= models.ForeignKey("User",on_delete=models.DO_NOTHING)
#     group_id= models.ForeignKey("Group", on_delete=models.DO_NOTHING)
    
#     def __str__(self):
#         return self.group_id
    
#     class Meta:
#         db_table = 'user_group'



# class GroupEvent(TimestampedModel):
#     group_id = models.ForeignKey("Group", on_delete=models.CASCADE)
#     event_id = models.ForeignKey("Event", on_delete=models.CASCADE)

#     def __str__(self):
#         return self.group_id

#     class Meta:
#         db_table = 'group_events'


# class GroupImage(TimestampedModel):
#     group_id = models.ForeignKey("Group", on_delete=models.CASCADE)
#     image_id = models.ForeignKey("Image", on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'group_image'

#     def __str__(self):
#         return self.group_id

    
# Interested Events Model
class InterestedEvent(TimestampedModel):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    event_id = models.ForeignKey("Event", on_delete=models.CASCADE)

    def __str__(self):
        return self.event_id
    class Meta:
        db_table = 'interested_events'


class Likes(TimestampedModel):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    comment_id = models.ForeignKey("Comment", on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_id

    class Meta:
        db_table = 'likes'


class PeopleGroup(Group):
    image = models.ImageField(("Group Image"))
    members = models.ManyToManyField(User)