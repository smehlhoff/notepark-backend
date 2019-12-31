from rest_framework import status
from rest_framework.test import APITestCase

from backend.users.models import User


class TestUser(APITestCase):
    def test_user_signup_success(self):
        """
        Test user sign up with valid data
        :return: HTTP 200
        """

        url = '/v1/users/'
        data = {
            'username': 'test',
            'email': 'test@example.com',
            'password': 'test12345',
            'confirm_password': 'test12345'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_user_signup_fail(self):
        """
        Test user sign up with invalid data
        :return: HTTP 400
        """

        url = '/v1/users/'
        data = {
            'username': '',
            'email': '',
            'password': '',
            'confirm_password': ''
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
