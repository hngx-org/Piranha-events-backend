from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=250, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.CharField(max_length=255)
    oauth_token = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    body = models.TextField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    """comment on event fields to be removed once event model is available"""
    # event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)