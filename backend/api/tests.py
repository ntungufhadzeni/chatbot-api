from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestSetUp(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', email='user@foo.com', password='password')
        user.save()
        self.access_token_url = reverse('token_obtain_pair')
        self.refresh_token_url = reverse('token_refresh')
        resp = self.client.post(self.access_token_url,
                                {'username': 'user', 'email': 'user@foo.com', 'password': 'password'}, format='json')
        self.token = resp.data['access']
        self.refresh_token = resp.data['refresh']


class TestToken(TestSetUp):
    def test_jwt_with_invalid_credentials(self):
        resp = self.client.post(self.access_token_url,
                                {'username': 'user1', 'email': 'user1@foo.com', 'password': 'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_with_valid_credentials(self):
        resp = self.client.post(self.access_token_url,
                                {'username': 'user', 'email': 'user@foo.com', 'password': 'password'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data)
        self.assertTrue('refresh' in resp.data)

    def test_refresh_token_with_valid_refresh(self):
        resp = self.client.post(self.refresh_token_url, {'refresh': self.refresh_token}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data)


class TestChat(TestSetUp):
    def test_chat_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(reverse('logout'), {"refresh_token": self.refresh_token}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_205_RESET_CONTENT)

    def test_chat_without_token(self):
        resp = self.client.get(reverse('chat'))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chat_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.get(reverse('chat'), format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_chat_post_with_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(reverse('chat'), {'data': 'hello'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_chat_post_with_valid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        resp = self.client.post(reverse('chat'), {'text': 'hello'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.json(), {'text': 'Hello, I am Chatty. Ask me some questions.'})
