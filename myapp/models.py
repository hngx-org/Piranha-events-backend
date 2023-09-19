from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
# Create your models here.



class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=250, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


# Interested Events Model
class InterestedEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)

    def __str__(self):
        # Doubt this will work. Test to see.
        return self.event.name

# Images Model
class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    comment = models.ForeignKey("comment", on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return self.image_id

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    body = models.TextField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.ForeignKey("Event", on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.username



class Group(models.Model):
    """model for group resource"""
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=20 )
    description= models.CharField(max_length=100)
    owner_id= models.ForeignKey("User", on_delete=models.DO_NOTHING)
    created_at= models.DateField(auto_now_add=True)

    def __str__(self):
        return self.group_name


class User_group(models.Model):
    """model for the user group object"""
    user= models.ForeignKey("User",on_delete=models.DO_NOTHING)
    event= models.ForeignKey("Event", on_delete=models.DO_NOTHING)



class Event(models.Model):
    """Model representing an event."""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=1024)
    creator_id = models.ForeignKey('User', on_delete=models.CASCADE)
    location = models.CharField(max_length=1024)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    thumbnail=models.ImageField(blank=True,upload_to='events/')

    class Meta:
        verbose_name ='Event'
        verbose_name_plural = ("Events")

    def __str__(self):
        """String for representing the Model object."""
        return self.title
