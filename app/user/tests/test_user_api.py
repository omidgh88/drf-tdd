from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payloads = {
            'email': 'test01@example.com',
            'password': 'pass123',
            'name': 'test 01 user'
        }
        res = self.client.post(CREATE_USER_URL, payloads)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payloads['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """test creating a user that already exists fail
        """
        payloads = {
            'email': 'test01@example.com',
            'password': 'pass123',
            'name': 'test 01 user'
        }
        create_user(**payloads)

        res = self.client.post(CREATE_USER_URL, payloads)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        payloads = {
            'email': 'test01@example.com',
            'password': 'pass123',
            'name': 'test 01 user'
        }
        create_user(**payloads)

        res = self.client.post(TOKEN_URL, payloads)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
