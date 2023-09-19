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
    



class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=20 )
    description= models.CharField(max_length=100)
    owner_id= models.ForeignKey(User.user_id)
    created_at= models.DateField(auto_now_add=True)

    def __str__(self):
        return self.group_name


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name= models.CharField(max_length=50)
    start_date= models.DateField(auto_now_add=True)
    end_date= models.DateField()
    locaion= models.CharField(max_length=100)
    description= models.CharField(max_length=100)

    def __str__(self):
        return self.event_name

class User_group(models.Model):
    user= models.ForeignKey(User)
    event= models.ForeignKey(Event)

