from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Event, Comment, Image  
import datetime

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

    # def test_get_event_details(self):
    #     event = Event.objects.create(title='Test Event', description='Test description')
    #     url = reverse('event-detail', args=[event.id])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_event_details(self):
    #     event = Event.objects.create(title='Test Event', description='Test description')
    #     url = reverse('event-detail', args=[event.id])
    #     data = {'title': 'Updated Event Name', 'description': 'Updated description'}
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete_event(self):
    #     event = Event.objects.create(title='Test Event', description='Test description')
    #     url = reverse('event-detail', args=[event.id])
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_add_comment_to_event(self):
    #     event = Event.objects.create(title='Test Event', description='Test description')
    #     url = reverse('comment-list', args=[event.id])
    #     data = {'text': 'Test Comment'}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_get_comments_for_event(self):
    #     event = Event.objects.create(title='Test Event', description='Test description')
    #     comment = Comment.objects.create(event=event, text='Test Comment')
    #     url = reverse('comment-list', args=[event.id])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_add_image_to_comment(self):
    #     comment = Comment.objects.create(text='Test Comment')
    #     url = reverse('image-list', args=[comment.id])
    #     # Add image data in the request
    #     response = self.client.post(url, {}, format='multipart')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_get_images_for_comment(self):
    #     comment = Comment.objects.create(text='Test Comment')
    #     image = Image.objects.create(comment=comment, image_url='image_url.jpg')
    #     url = reverse('image-list', args=[comment.id])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
