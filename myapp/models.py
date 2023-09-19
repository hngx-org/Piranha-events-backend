from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.


class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=250, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.CharField(max_length=255)
    oauth_token = models.CharField(max_length=255)

    def __str__(self):
        return self.username

# Interested Events Model
class interestedEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Should be uncommented when event model is created.
    # event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        # This should display the event's name (Probably).
        return self.event.name

# Images Model
# 'Pillow' module will need to be installed for this to work.
class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    # Should be uncommented when comment model exists.
    # comment = models.ForeignKey(comment, on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        # I don't really know what should be returned.
        return self.image_id
