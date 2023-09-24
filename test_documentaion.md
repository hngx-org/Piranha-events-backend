# A Detailed Tests Documentaion of Team Piranha Event app Endpoints

## Table of Contents

- [LoginViewTest](#loginviewtestcase)
  - [test_login_successful](#test_login_successful)
  - [test_user_login](#test_user_login)
  - [test_get_user_profile](#test_get_user_profile)
  - [test_update_user_profile](#test_update_user_profile)

- [EventAPITestCase](#eventapitestcase)
  - [test_create_event](#test_create_event)
  - [test_get_event_list](#test_get_event_list)
  - [test_get_event_details](#test_get_event_details)
  - [test_update_event_details](#test_update_event_details)
  - [test_delete_event](#test_delete_event)
  - [test_add_comment_to_event](#test_add_comment_to_event)
  - [test_get_comments_for_event](#test_get_comments_for_event)
  - [test_add_image_to_comment](#test_add_image_to_comment)
  - [test_get_images_for_comment](#test_get_images_for_comment)

- [CommentViewTestCases](#commentviewtestcases)
  - [test_create_comment](#test_create_comment)
  - [test_list_comments](#test_list_comments)
  - [test_retrieve_comment](#test_retrieve_comment)
  - [test_update_comment](#test_update_comment)
  - [test_destroy_comment](#test_destroy_comment)

- [GroupViewTestCases](#groupviewtestcases)
  - [test_create_group](#test_create_group)
  - [test_list_groups](#test_list_groups)
  - [test_retrieve_group](#test_retrieve_group)
  - [test_update_group](#test_update_group)

- [LikeViewTestCase and DeleteLikeViewTestCase](#likeviewtestcase-and-deletelikeviewtestcase)
  - [test_create_like](#test_create_like-in-likeviewtestcase)
  - [test_create_like_unauthenticated](#test_create_like_unauthenticated-in-likeviewtestcase)
  - [test_create_like_duplicate](#test_create_like_duplicate-in-likeviewtestcase)
  - [test_delete_like](#test_delete_like-in-deletelikeviewtestcase)
  - [test_delete_like_unauthenticated](#test_delete_like_unauthenticated-in-deletelikeviewtestcase)
  - [test_delete_like_nonexistent](#test_delete_like_nonexistent-in-deletelikeviewtestcase)

#### *NOTE: Update the tests you have written inline with the reviewed class-based views and make updates to this document*

# UserManagementAPITest
This test suite is responsible for testing user management-related APIs.

## test_user_registration
**Description:** This test case checks the user registration endpoint by sending a POST request to `/api/login/`.

**Expected Behavior:**
- Response Status Code: 201 (Created)
- Response JSON contains a `user_id` and `username`.

## test_user_login
**Description:** This test case checks the user login endpoint by sending a POST request to `/api/login/`.

**Expected Behavior:**
- Response Status Code: 200 (OK)
- Response JSON contains a `token`.

## test_get_user_profile
**Description:** This test case checks the get user profile endpoint by sending a GET request to `/api/users/profile`.

**Expected Behavior:**
- Response Status Code: 200 (OK)
- Response JSON contains a `user_id`.

## test_update_user_profile
**Description:** This test case checks the update user profile endpoint by sending a PUT request to `/api/users/profile`.

**Expected Behavior:**
- Response Status Code: 200 (OK)
- Response JSON contains the updated email.

# EventAPITestCase
This test suite is responsible for testing event-related APIs.

## test_create_event
**Description:** This test case checks the creation of an event by sending a POST request to the event creation endpoint - `/api/event`.

**Expected Behavior:**
- Response Status Code: 201 (Created)

## test_get_event_list
**Description:** This test case checks the retrieval of a list of events by sending a GET request to the event list endpoint - `/api/event`.

**Expected Behavior:**
- Response Status Code: 200 (OK)

## test_get_event_details
**Description:** This test case checks the retrieval of event details by sending a GET request to the event detail endpoint - ``.

**Expected Behavior:**
- Response Status Code: 200 (OK)

## test_update_event_details
**Description:** This test case checks the update of event details by sending a PUT request to the event detail endpoint - ``.

**Expected Behavior:**
- Response Status Code: 200 (OK)

## test_delete_event
**Description:** This test case checks the deletion of an event by sending a DELETE request to the event detail endpoint - ``.

**Expected Behavior:**
- Response Status Code: 204 (No Content)

## test_add_comment_to_event
**Description:** This test case checks adding a comment to an event by sending a POST request to the comment creation endpoint.

**Expected Behavior:**
- Response Status Code: 201 (Created)

## test_get_comments_for_event
**Description:** This test case checks retrieving comments for an event by sending a GET request to the comment list endpoint.

**Expected Behavior:**
- Response Status Code: 200 (OK)

## test_add_image_to_comment
**Description:** This test case checks adding an image to a comment by sending a POST request to the image creation endpoint.

**Expected Behavior:**
- Response Status Code: 201 (Created)

## test_get_images_for_comment
**Description:** This test case checks retrieving images for a comment by sending a GET request to the image list endpoint.

**Expected Behavior:**
- Response Status Code: 200 (OK)

# CommentViewTestCases
This test suite is responsible for testing comment-related APIs.

## test_create_comment
**Description:** This test case checks creating a new comment.

**Expected Behavior:**
- Response Status Code: 201 (Created)

## test_list_comments
**Description:** This test case checks listing comments.

**Expected Behavior:**
- Response Status Code: 200 (OK)

## test_retrieve_comment
**Description:** This test case checks retrieving a specific comment.

**Expected Behavior:**
- Response Status Code: 200 (OK)

## test_update_comment
**Description:** This test case checks updating a comment.

**Expected Behavior:**
- Response Status Code: 200 (OK)

## test_destroy_comment
**Description:** This test case checks deleting a comment.

**Expected Behavior:**
- Response Status Code: 204 (No Content)

# GroupViewTestCases
This test suite is responsible for testing group-related APIs.

## test_create_group
**Description:** This test case checks creating a new group.

**Expected Behavior:**
- Response Status Code: 201 (Created)

## test_list_groups
**Description:** This test case checks listing groups.

**Expected Behavior:**
- Response Status Code: 200 (OK)

## test_retrieve_group
**Description:** This test case checks retrieving a specific group.

**Expected Behavior:**
- Response Status Code: 200 (OK)

## test_update_group
**Description:** This test case checks updating a group.

**Expected Behavior:**
- Response Status Code: 200 (OK)

# LikeViewTestCase and DeleteLikeViewTestCase
This test suite is responsible for testing like-related APIs.

## test_create_like (in LikeViewTestCase)
**Description:** This test case checks creating a like for an event - `/api/like`.

**Expected Behavior:**
- Response Status Code: 201 (Created)

## test_create_like_unauthenticated (in LikeViewTestCase)
**Description:** This test case checks creating a like by an unauthenticated user.

**Expected Behavior:**
- Response Status Code: 401 (Unauthorized)
- Response JSON contains a message indicating the need to be signed in.

## test_create_like_duplicate (in LikeViewTestCase)
**Description:** This test case checks creating a duplicate like.

**Expected Behavior:**
- Response Status Code: 400 (Bad Request)
- Response JSON contains a message indicating that double liking is not allowed.

## test_delete_like (in DeleteLikeViewTestCase)
**Description:** This test case checks deleting a like - `/api/like/id`.

**Expected Behavior:**
- Response Status Code: 204 (No Content)
- The like is successfully deleted.

## test_delete_like_unauthenticated (in DeleteLikeViewTestCase)
**Description:** This test case checks deleting a like by an unauthenticated user.

**Expected Behavior:**
- Response Status Code: 401 (Unauthorized)
- The like is not deleted.

## test_delete_like_nonexistent (in DeleteLikeViewTestCase)
**Description:** This test case checks deleting a non-existent like.

**Expected Behavior:**
- Response Status Code: 404 (Not Found)
- Response JSON contains a message indicating that the like does not exist.
