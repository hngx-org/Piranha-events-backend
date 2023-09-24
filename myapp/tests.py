import datetime
import unittest
import requests
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
# from .models import Event, Comment, User, Likes, PeopleGroup #Group, UserGroup

from .model import *
from django.contrib.auth.models import User
from .config import BASE_URL


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_url = reverse('login-group')

    def test_login_successful(self):
        # Prepare test data
        data = {
            'email': 'test@example.com',
            'pass_id': 'password123'
        }

        # Send a POST request to the login view
        response = self.client.post(self.base_url, data, format='json')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Login successful')
        self.assertIsNotNone(response.data['data']['token'])
        self.assertIsNotNone(response.data['data']['id'])
        self.assertIsNotNone(response.data['data']['name'])
        self.assertIsNotNone(response.data['data']['email'])

        # Check if a user with the provided email exists in the database
        user = User.objects.filter(email=data['email']).first()
        self.assertIsNotNone(user)

    def test_login_failed(self):
        # Prepare test data with missing fields
        data = {
            'email': 'test@example.com',
        }

        # Send a POST request to the login view with incomplete data
        response = self.client.post(self.base_url, data, format='json')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content for errors
        self.assertEqual(response.data['status'], 'Failed, something went wrong')
        self.assertIn('pass_id', response.data['message'])

        # Ensure that a user with the provided email does not exist in the database
        user = User.objects.filter(email=data['email']).first()
        self.assertIsNone(user)


"""
single group view | path('group/<int:id>/', SingleGroupView.as_view(), name='single-group')
"""
class SingleGroupViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_existing_group(self):
        # Create a PeopleGroup instance for testing
        group = PeopleGroup.objects.create(name="Test Group")
        
        # Send a GET request to retrieve the group by ID
        response = self.client.get(f'{BASE_URL}/api/group/{group.id}/')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Test Group fetched successfully!')
        self.assertEqual(response.data['data']['name'], 'Test Group')

    def test_get_nonexistent_group(self):
        # Send a GET request to retrieve a non-existent group by ID
        response = self.client.get(f'{BASE_URL}/api/groups/999/')  # Assuming 999 does not exist

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        self.assertEqual(response.data['status'], 'Failed, something went wrong')
        self.assertEqual(response.data['message'], 'Group does not exist')

    def test_get_group_with_members(self):
        # Create a PeopleGroup instance with members for testing
        group = PeopleGroup.objects.create(name="Group with Members")
        member1 = Member.objects.create(name="Member 1", group=group)
        member2 = Member.objects.create(name="Member 2", group=group)
        
        # Send a GET request to retrieve the group by ID
        response = self.client.get(f'{BASE_URL}/api/groups/{group.id}/')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Group with Members fetched successfully!')
        self.assertEqual(response.data['data']['name'], 'Group with Members')
        self.assertEqual(len(response.data['data']['members']), 2)  # Check the number of members

    def test_get_group_with_invalid_id(self):
        # Send a GET request with an invalid group ID
        response = self.client.get(f'{BASE_URL}/api/groups/{342}/')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        self.assertEqual(response.data['status'], 'Failed, something went wrong')
        self.assertIn('Group does not exist', response.data['message'])

    def test_get_group_with_invalid_input(self):
        # Send a GET request without specifying an ID (invalid input)
        response = self.client.get(f'{BASE_URL}/api/groups/')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_group_with_empty_members(self):
        # Create a PeopleGroup instance without members for testing
        group = PeopleGroup.objects.create(name="Group without Members")
        
        # Send a GET request to retrieve the group by ID
        response = self.client.get(f'{BASE_URL}/api/groups/{group.id}/')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Group without Members fetched successfully!')
        self.assertEqual(response.data['data']['name'], 'Group without Members')
        self.assertEqual(len(response.data['data']['members']), 0)  # Check the number of members


"""add user to group
"""
class AddUserGroupViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.group = PeopleGroup.objects.create(name="Test Group")
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_add_user_to_group_successful(self):
        data = {
            'user_id': self.user.id,
            'group_id': self.group.id,
        }

        response = self.client.post(f'{BASE_URL}/api/add_user/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the user is added to the group
        self.assertTrue(self.group.user_set.filter(id=self.user.id).exists())

    def test_add_user_to_nonexistent_group(self):
        data = {
            'user_id': self.user.id,
            'group_id': 999,  # Assuming this group does not exist
        }

        response = self.client.post(f'{BASE_URL}/api/add_user/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check the response content
        self.assertEqual(response.data['status'], 'Failed, something went wrong')

    def test_add_nonexistent_user_to_group(self):
        data = {
            'user_id': 999,  # Assuming this user does not exist
            'group_id': self.group.id,
        }

        response = self.client.post(f'{BASE_URL}/api/add_user/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check the response content
        self.assertEqual(response.data['status'], 'Failed, something went wrong')

    def test_add_user_to_group_with_invalid_data(self):
        data = {
            'user_id': 'invalid',  # Invalid user_id
            'group_id': self.group.id,
        }

        response = self.client.post(f'{BASE_URL}/api/add_user/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content for serializer errors
        self.assertIn('user_id', response.data['message'])

    def test_add_user_to_group_with_missing_data(self):
        data = {}  # Missing user_id and group_id

        response = self.client.post(f'{BASE_URL}/api/add_user/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content for serializer errors
        self.assertIn('user_id', response.data['message'])
        self.assertIn('group_id', response.data['message'])


"""removes user from a group: /api/group/remove_user/
"""
class RemoveUserGroupViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.group = PeopleGroup.objects.create(name="Test Group")
        self.user = User.objects.create_user(username='testuser', password='password')
        self.group.user_set.add(self.user)
        self.group.members.add(self.user)

    def test_remove_user_from_group_successful(self):
        data = {
            'user_id': self.user.id,
            'group_id': self.group.id,
        }

        response = self.client.post(f'{BASE_URL}/api/group/remove_user/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the user is removed from the group
        self.assertFalse(self.group.user_set.filter(id=self.user.id).exists())

    def test_remove_nonexistent_user_from_group(self):
        data = {
            'user_id': 999,  # Assuming this user does not exist
            'group_id': self.group.id,
        }

        response = self.client.post(f'{BASE_URL}/api/group/remove_user/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check the response content
        self.assertEqual(response.data['status'], 'Failed, something went wrong')

    def test_remove_user_from_nonexistent_group(self):
        data = {
            'user_id': self.user.id,
            'group_id': 999,  # Assuming this group does not exist
        }

        response = self.client.post(f'{BASE_URL}/api/group/remove_user/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check the response content
        self.assertEqual(response.data['status'], 'Failed, something went wrong')

    def test_remove_user_from_group_with_invalid_data(self):
        data = {
            'user_id': 'invalid',  # Invalid user_id
            'group_id': self.group.id,
        }

        response = self.client.post(f'{BASE_URL}/api/group/remove_user/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content for serializer errors
        self.assertIn('user_id', response.data['message'])

    def test_remove_user_from_group_with_missing_data(self):
        data = {}  # Missing user_id and group_id

        response = self.client.post(f'{BASE_URL}/api/group/remove_user/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content for serializer errors
        self.assertIn('user_id', response.data['message'])
        self.assertIn('group_id', response.data['message'])


"""creates a new group: /api/group/
"""
class CreateGroupViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_create_group_successful(self):
        data = {
            'name': 'Test Group',
            'user': self.user.id,
        }

        response = self.client.post(f'{BASE_URL}/api/group/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the group is created and the user is added to it
        self.assertTrue(PeopleGroup.objects.filter(name='Test Group').exists())
        group = PeopleGroup.objects.get(name='Test Group')
        self.assertTrue(group.user_set.filter(id=self.user.id).exists())

    def test_create_group_with_invalid_user(self):
        data = {
            'name': 'Test Group',
            'user': 999,  # Assuming this user does not exist
        }

        response = self.client.post(f'{BASE_URL}/api/group/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        self.assertEqual(response.data['status'], 'failed')

    def test_create_group_with_invalid_data(self):
        data = {
            'name': '',  # Invalid empty name
            'user': self.user.id,
        }

        response = self.client.post(f'{BASE_URL}/api/group/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content for serializer errors
        self.assertIn('name', response.data['message'])

    def test_create_group_with_missing_data(self):
        data = {}  # Missing name and user

        response = self.client.post(f'{BASE_URL}/api/group/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content for serializer errors
        self.assertIn('name', response.data['message'])
        self.assertIn('user', response.data['message'])


class DeleteGroupViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.group = PeopleGroup.objects.create(name="Test Group")

    def test_delete_group_successful(self):
        response = self.client.delete(f'{BASE_URL}/api/group/{self.group.id}/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the group has been deleted
        self.assertFalse(PeopleGroup.objects.filter(id=self.group.id).exists())

    def test_delete_nonexistent_group(self):
        non_existent_group_id = self.group.id + 1  # Assuming this group does not exist

        response = self.client.delete(f'{BASE_URL}/api/group/{non_existent_group_id}/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        self.assertEqual(response.data['status'], 'failed')


"""view a group a user belongs to
"""
class UserGroupViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.group = PeopleGroup.objects.create(name="Test Group")
        self.group.members.add(self.user)

    def test_fetch_groups_for_existing_user(self):
        response = self.client.get(f'{BASE_URL}/api/group/user/{self.user.id}/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('data', response.data)
        self.assertTrue(len(response.data['data']) > 0)

    def test_fetch_groups_for_user_with_no_groups(self):
        no_groups_user = User.objects.create_user(username='nogroups', password='password')

        response = self.client.get(f'{BASE_URL}/api/group/user/{no_groups_user.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User does not belong to any group')

    def test_fetch_groups_for_nonexistent_user(self):
        non_existent_user_id = self.user.id + 1  # Assuming this user does not exist

        response = self.client.get(f'{BASE_URL}/api/group/user/{non_existent_user_id}/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        self.assertEqual(response.data['status'], 'failed')


"""create an event
"""
class CreateEventViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.group = PeopleGroup.objects.create(name="Test Group")

    def test_create_event_successful(self):
        data = {
            'title': 'Test Event',
            'description': 'Description for the event',
            'location': 'Event Location',
            'start_time': '2023-09-30T10:00:00Z',
            'end_time': '2023-09-30T12:00:00Z',
            'group': self.group.id,
            'owner': self.user.id,
            'thumbnail': None  # Replace with the actual thumbnail data if needed
        }

        response = self.client.post(f'{BASE_URL}/api/event/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('data', response.data)
        self.assertEqual(response.data['message'], 'New Event (Test Event) created successfully!')

        # Check if the event has been created in the database
        self.assertTrue(Event.objects.filter(title='Test Event').exists())

    def test_create_event_invalid_data(self):
        data = {
            # Missing required fields, which should make the data invalid
        }

        response = self.client.post(f'{BASE_URL}/api/event/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        self.assertEqual(response.data['status'], 'Failed, something went wrong')
        self.assertIn('message', response.data)

        # Check if the event has not been created in the database
        self.assertFalse(Event.objects.filter(title='Test Event').exists())


"""view all available event
"""
class AllEventViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.event = Event.objects.create(title="Test Event")

    def test_fetch_all_events_successful(self):
        response = self.client.get(f'{BASE_URL}/api/events/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('data', response.data)
        self.assertTrue(len(response.data['data']) > 0)

    def test_fetch_all_events_empty(self):
        # Delete the test event, so there are no events in the database
        self.event.delete()

        response = self.client.get(f'{BASE_URL}/api/events/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'All events fetched successfully!')

    def test_fetch_all_events_exception(self):
        # Simulate an exception by making the queryset raise an error
        with self.assertRaises(Exception):
            response = self.client.get(f'{BASE_URL}/api/events/')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            # Check the response content
            self.assertEqual(response.data['status'], 'failed')


class SingleEventViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.event = Event.objects.create(title="Test Event")

    def test_fetch_existing_event(self):
        response = self.client.get(f'{BASE_URL}/api/event/{self.event.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('data', response.data)
        self.assertEqual(response.data['message'], 'Event retrieved')

    def test_fetch_nonexistent_event(self):
        nonexistent_event_id = self.event.id + 1  # Assuming this event does not exist

        response = self.client.get(f'{BASE_URL}/api/event/{nonexistent_event_id}/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        self.assertEqual(response.data['status'], 'failed')


"""view all event particular to a user"""
class UserEventViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.group = PeopleGroup.objects.create(name="Test Group")
        self.group.members.add(self.user)
        self.event = Event.objects.create(title="Test Event", group=self.group)

    def test_fetch_events_for_existing_user(self):
        response = self.client.get(f'{BASE_URL}/api/event/user/{self.user.id}/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('data', response.data)
        self.assertTrue(len(response.data['data']) > 0)

    def test_fetch_events_for_user_with_no_groups(self):
        no_groups_user = User.objects.create_user(username='nogroups', password='password')

        response = self.client.get(f'{BASE_URL}/api/event/user/{no_groups_user.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User does not belong to any group')

    def test_fetch_events_for_nonexistent_user(self):
        non_existent_user_id = self.user.id + 1  # Assuming this user does not exist

        response = self.client.get(f'{BASE_URL}/api/event/user/{non_existent_user_id}/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        self.assertEqual(response.data['status'], 'failed')


"""test for event comments
"""
class CreateEventCommentViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_create_comment_successful(self):
        data = {
            'text': 'This is a test comment',
            'event': None,  # Replace with an actual event ID if needed
            'author': self.user.id
        }

        response = self.client.post(f'{BASE_URL}/api/comment/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('data', response.data)
        self.assertEqual(response.data['message'], 'Comment added successfully!')

        # Check if the comment has been created in the database
        self.assertTrue(Comment.objects.filter(text='This is a test comment').exists())

    def test_create_comment_invalid_data(self):
        data = {
            # Missing required fields, which should make the data invalid
        }

        response = self.client.post(f'{BASE_URL}/api/comment/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        self.assertEqual(response.data['status'], 'Failed something went wrong')
        self.assertIn('message', response.data)

        # Check if the comment has not been created in the database
        self.assertFalse(Comment.objects.filter(text='This is a test comment').exists())


"""
Testcase for LikeView
"""
class LikeViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.event = Event.objects.create(
            title="Test Event",
            description="This is a test event",
            location="Test Location",
            start_time="2023-09-25T12:00:00Z",
            end_time="2023-09-25T14:00:00Z",
            group=None,  # You can set this to a group if needed
            owner=self.user,
            thumbnail=None,  # You can add a thumbnail if needed
        )

    def test_create_like(self):
        # test user create like endpoint /api/like/
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            f"{BASE_URL}/api/like/",
            {
                "user_id": self.user.id,
                "event_id": self.event.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Likes.objects.count(), 1)

    def test_create_like_unauthenticated(self):
        """validates likes by an unauthenticated user"""
        response = self.client.post(
            f"{BASE_URL}/api/like/",
            {
                "user_id": self.user.id,
                "event_id": self.event.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], "You must be signed in to like")

    def test_create_like_duplicate(self):
        """validates duplicated likes"""
        self.client.force_authenticate(user=self.user)
        Likes.objects.create(user=self.user, event=self.event)  # Create a like
        response = self.client.post(
            f"{BASE_URL}/api/like/",
            {
                "user_id": self.user.id,
                "event_id": self.event.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Cannot double like")


"""
Testcase for DeleteLikeView
"""
class DeleteLikeViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.event = Event.objects.create(
            title="Test Event",
            description="This is a test event",
            location="Test Location",
            start_time="2023-09-25T12:00:00Z",
            end_time="2023-09-25T14:00:00Z",
            group=None,  # You can set this to a group if needed
            owner=self.user,
            thumbnail=None,  # You can add a thumbnail if needed
        )
        self.like = Likes.objects.create(user=self.user, event=self.event)

    def test_delete_like(self):
        """validate delete or undo of a like endpoint /api/like/id/"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"{BASE_URL}/api/like/{self.like.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Likes.objects.count(), 0)

    def test_delete_like_unauthenticated(self):
        """check for is a like is created by a user not authenticated"""
        response = self.client.delete(f"{BASE_URL}/api/like/{self.like.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Likes.objects.count(), 1)

    def test_delete_like_nonexistent(self):
        """validates deletetion on like_id which dosent exist"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"{BASE_URL}/api/like/999/")  # Non-existent like ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "Like does not exist")


class InterestEventViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_show_interest_successful(self):
        data = {
            'user': self.user.id,
            'event': None,  # Replace with an actual event ID if needed
        }

        response = self.client.post(f'{BASE_URL}/api/interested_event/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('data', response.data)
        self.assertEqual(response.data['message'], 'Interest has been shown in event')

        # Check if the interest has been created in the database
        self.assertTrue(InterestedEvent.objects.filter(user=self.user).exists())

    def test_show_interest_invalid_data(self):
        data = {
            # Missing required fields, which should make the data invalid
        }

        response = self.client.post(f'{BASE_URL}/api/interested_event/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        self.assertEqual(response.data['status'], 'Failed, something went wrong')
        self.assertIn('message', response.data)

        # Check if the interest has not been created in the database
        self.assertFalse(InterestedEvent.objects.filter(user=self.user).exists())


class InterestDeleteEventViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.interest_event = InterestedEvent.objects.create(user=self.user, event=None)  # Replace with an actual event if needed

    def test_revoke_interest_successful(self):
        response = self.client.delete(f'{BASE_URL}/api/interested_event/{self.interest_event.id}/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Interest in event revoked')

        # Check if the interest has been deleted from the database
        self.assertFalse(InterestedEvent.objects.filter(id=self.interest_event.id).exists())

    def test_revoke_nonexistent_interest(self):
        nonexistent_interest_id = self.interest_event.id + 1  # Assuming this interest does not exist

        response = self.client.delete(f'{BASE_URL}/api/interested_event/{nonexistent_interest_id}/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        self.assertEqual(response.data['status'], 'failed')
        self.assertIn('message', response.data)

        # Check if the interest has not been deleted from the database
        self.assertTrue(InterestedEvent.objects.filter(id=self.interest_event.id).exists())


class EventInterestUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.event = None  # Replace with an actual event if needed
        self.interest_event = InterestedEvent.objects.create(user=self.user, event=self.event)

    def test_get_interested_users_successful(self):
        response = self.client.get(f'{BASE_URL}/api/interested_event/event/{self.event.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('data', response.data)
        self.assertEqual(response.data['message'], 'Interested users retrieved')

        # Check if the interested user is in the response data
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['user'], self.user.id)

    def test_get_interested_users_for_nonexistent_event(self):
        nonexistent_event_id = self.event.id + 1  # Assuming this event does not exist

        response = self.client.get(f'{BASE_URL}/api/interested_event/event/{nonexistent_event_id}/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        self.assertEqual(response.data['status'], 'failed')
        self.assertIn('message', response.data)

        # Check if the response data is empty
        self.assertEqual(len(response.data['data']), 0)


class AcceptInterestEventViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.event = None  # Replace with an actual event if needed
        self.interest_event = InterestedEvent.objects.create(user=self.user, event=self.event)

    def test_accept_interest_successful(self):
        response = self.client.post(f'{BASE_URL}/api/interested_event/accept/{self.interest_event.id}/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the response content
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], f"{self.user.username} has been invited to {self.event.group.name}")

        # Check if the interest has been deleted from the database
        self.assertFalse(InterestedEvent.objects.filter(id=self.interest_event.id).exists())

        # Check if the user has been added to the group
        self.assertTrue(self.event.group.user_set.filter(id=self.user.id).exists())
        self.assertTrue(self.event.group.members.filter(id=self.user.id).exists())

    def test_accept_nonexistent_interest(self):
        nonexistent_interest_id = self.interest_event.id + 1  # Assuming this interest does not exist

        response = self.client.post(f'{BASE_URL}/api/interested_event/accept/{nonexistent_interest_id}/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        self.assertEqual(response.data['status'], 'Failed')
        self.assertIn('message', response.data)

        # Check if the interest has not been deleted from the database
        self.assertTrue(InterestedEvent.objects.filter(id=self.interest_event.id).exists())

    def test_accept_interest_user_not_found(self):
        # Set the user ID to an ID that doesn't exist
        self.interest_event.user_id = User.objects.last().id + 1  # Assuming this user doesn't exist

        response = self.client.post(f'{BASE_URL}/api/interested_event/accept/{self.interest_event.id}/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        self.assertEqual(response.data['status'], 'Failed')
        self.assertIn('message', response.data)

        # Check if the interest has not been deleted from the database
        self.assertTrue(InterestedEvent.objects.filter(id=self.interest_event.id).exists())
