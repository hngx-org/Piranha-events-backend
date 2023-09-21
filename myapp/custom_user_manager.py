"""This module defines the class CustomUserManager"""
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """This class defines the create_user and create_superuser methods."""
    def create_user(self, username, email, password, **other_fields):
        """This method creates a user and saves it in the database."""
        if not username:
            raise ValueError('username is required.')
        if not email:
            raise ValueError('email is required.')
        if not password:
            raise ValueError('password is required.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, password=password, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **other_fields):
        """This method creates a super user."""
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **other_fields)
