from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from rest_framework import status
import json

User = get_user_model()


class UserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Иван',
            last_name='Иванов'
        )
        self.moderator = User.objects.create_user(
            email='moderator@example.com',
            password='moder123'
        )
        moder_group = Group.objects.get_or_create(name='Модераторы')[0]
        self.moderator.groups.add(moder_group)

    def test_user_registration(self):
        """Тест регистрации пользователя"""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'first_name': 'Новый',
            'last_name': 'Пользователь'
        }
        response = self.client.post(
            '/api/auth/register/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'newuser@example.com')

    def test_jwt_token_obtain(self):
        """Тест получения JWT токена"""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(
            '/api/auth/token/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_jwt_token_refresh(self):
        """Тест обновления JWT токена"""
        # Сначала получаем токен
        data = {'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post(
            '/api/auth/token/',
            data=json.dumps(data),
            content_type='application/json'
        )
        refresh_token = response.data['refresh']

        # Обновляем токен
        data = {'refresh': refresh_token}
        response = self.client.post(
            '/api/auth/token/refresh/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_profile_get(self):
        """Тест получения профиля пользователя"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_user_profile_update(self):
        """Тест обновления профиля"""
        self.client.force_authenticate(user=self.user)
        data = {'first_name': 'Обновленное имя', 'city': 'Москва'}
        response = self.client.patch(
            '/api/auth/profile/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Обновленное имя')

    def test_user_list_only_for_moderators(self):
        """Тест: список пользователей доступен только модераторам"""
        # Обычный пользователь не должен видеть список
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/auth/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Модератор должен видеть список
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get('/api/auth/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_without_authentication(self):
        """Тест доступа без аутентификации"""
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

