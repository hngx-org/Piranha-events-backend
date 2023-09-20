
import unittest
import requests
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Event, Comment, Image  
import datetime

class UserManagementAPITest(unittest.TestCase):
    base_url = "http://localhost:8000/api/users"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user_registration(self):
        # Test user registration endpoint (POST /api/users/register)
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "avatar": "default_avatar.png",
            "oauth_token": "test_token"
        }

        response = requests.post(f"{self.base_url}/register", json=data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn("user_id", response_data)
        self.assertEqual(response_data["username"], "testuser")

    def test_user_login(self):
        # Test user login endpoint (POST /api/users/login)
        data = {
            "username": "testuser",
            "password": "testpassword" # Replace with a valid password
        }

        response = requests.post(f"{self.base_url}/login", json=data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("token", response_data)

    def test_get_user_profile(self):
        # Test get user profile endpoint (GET /api/users/profile)

        headers = {}

        response = requests.get(f"{self.base_url}/profile", headers=headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("user_id", response_data)
        

    def test_update_user_profile(self):
        # Test update user profile endpoint (PUT /api/users/profile)

        headers = {}

        data = {
            "email": "newemail@example.com",
            "avatar": "new_avatar.png"
        }

        response = requests.put(f"{self.base_url}/profile", json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["email"], "newemail@example.com")
        


class EventAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_event(self):
        url = reverse('event-list')
        data = {
            "title": "'Test Event'",
            "description": "Test description",
            "creator_id": "", 
            "location": "London",
            "start_date": "2023-09-20",
            "end_date": "2023-09-21",
            "start_time": "2023-09-20T10:00:00Z",
            "end_time": "2023-09-21T12:00:00Z",
            "thumbnail": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_event_list(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_event_details(self):
        event = Event.objects.create(title='Test Event', description='Test description')
        url = reverse('event-detail', args=[event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_event_details(self):
        event = Event.objects.create(title='Test Event', description='Test description')
        url = reverse('event-detail', args=[event.id])
        data = {'title': 'Updated Event Name', 'description': 'Updated description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_event(self):
        event = Event.objects.create(title='Test Event', description='Test description')
        url = reverse('event-detail', args=[event.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_add_comment_to_event(self):
        event = Event.objects.create(title='Test Event', description='Test description')
        url = reverse('comment-list', args=[event.id])
        data = {'text': 'Test Comment'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_comments_for_event(self):
        event = Event.objects.create(title='Test Event', description='Test description')
        comment = Comment.objects.create(event=event, text='Test Comment')
        url = reverse('comment-list', args=[event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_image_to_comment(self):
        comment = Comment.objects.create(text='Test Comment')
        url = reverse('image-list', args=[comment.id])
        # Add image data in the request
        response = self.client.post(url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_images_for_comment(self):
        comment = Comment.objects.create(text='Test Comment')
        image = Image.objects.create(comment=comment, image_url='image_url.jpg')
        url = reverse('image-list', args=[comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
