import unittest
import requests

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
        

if __name__ == "__main__":
    unittest.main()
