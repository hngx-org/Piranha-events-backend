from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)

    def __str__(self):
        return self.name
