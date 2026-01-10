from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from lms.models import Course, Lesson, Subscription

User = get_user_model()


class BasicLessonTests(TestCase):
    """Базовые тесты для уроков"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.course = Course.objects.create(
            name='Тестовый курс',
            description='Описание курса',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name='Тестовый урок',
            description='Описание урока',
            video_url='https://www.youtube.com/watch?v=test123',
            course=self.course,
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson_success(self):
        """Тест успешного создания урока"""
        data = {
            'name': 'Новый урок',
            'description': 'Описание нового урока',
            'video_url': 'https://www.youtube.com/watch?v=abc123',
            'course': self.course.id
        }
        response = self.client.post(
            '/api/lessons/',
            data=data,  # format='json' автоматически сериализует
            format='json'
        )
        print(f"CREATE RESPONSE: {response.status_code} - {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_lesson_success(self):
        """Тест успешного обновления урока"""
        data = {
            'name': 'Обновленное название урока'
        }
        response = self.client.patch(
            f'/api/lessons/{self.lesson.id}/',
            data=data,
            format='json'
        )
        print(f"UPDATE RESPONSE: {response.status_code} - {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Обновленное название урока')

    def test_get_lessons_list(self):
        """Тест получения списка уроков"""
        response = self.client.get('/api/lessons/')
        print(f"LIST RESPONSE: {response.status_code} - Results: {len(response.data.get('results', []))}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_get_lesson_detail(self):
        """Тест получения деталей урока"""
        response = self.client.get(f'/api/lessons/{self.lesson.id}/')
        print(f"DETAIL RESPONSE: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BasicSubscriptionTests(TestCase):
    """Базовые тесты для подписок"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.course = Course.objects.create(
            name='Курс для подписки',
            description='Описание курса',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        """Тест подписки на курс"""
        data = {'course_id': self.course.id}
        response = self.client.post(
            '/api/subscriptions/',
            data=data,
            format='json'
        )
        print(f"SUBSCRIBE RESPONSE: {response.status_code} - {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsubscribe_from_course(self):
        """Тест отписки от курса"""
        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        data = {'course_id': self.course.id}
        response = self.client.post(
            '/api/subscriptions/',
            data=data,
            format='json'
        )
        print(f"UNSUBSCRIBE RESPONSE: {response.status_code} - {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class YouTubeValidationTests(TestCase):
    """Тесты валидации YouTube ссылок"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.course = Course.objects.create(
            name='Тестовый курс',
            description='Описание',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_youtube_url_valid(self):
        """Тест валидной YouTube ссылки"""
        data = {
            'name': 'Урок с YouTube ссылкой',
            'description': 'Описание',
            'video_url': 'https://www.youtube.com/watch?v=abc123',
            'course': self.course.id
        }
        response = self.client.post(
            '/api/lessons/',
            data=data,
            format='json'
        )
        print(f"VALID YOUTUBE RESPONSE: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_youtube_short_url_valid(self):
        """Тест валидной короткой YouTube ссылки"""
        data = {
            'name': 'Урок с короткой YouTube ссылкой',
            'description': 'Описание',
            'video_url': 'https://youtu.be/abc123',
            'course': self.course.id
        }
        response = self.client.post(
            '/api/lessons/',
            data=data,
            format='json'
        )
        print(f"SHORT YOUTUBE RESPONSE: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class BasicCourseTests(TestCase):
    """Базовые тесты для курсов"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.course = Course.objects.create(
            name='Тестовый курс',
            description='Описание курса',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        """Тест создания курса"""
        data = {
            'name': 'Новый курс',
            'description': 'Описание нового курса'
        }
        response = self.client.post(
            '/api/courses/',
            data=data,
            format='json'
        )
        print(f"CREATE COURSE RESPONSE: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_courses_list(self):
        """Тест получения списка курсов"""
        response = self.client.get('/api/courses/')
        print(f"COURSES LIST RESPONSE: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)


class AuthenticationTests(TestCase):
    """Тесты аутентификации"""

    def test_access_without_auth(self):
        """Тест доступа без аутентификации"""
        client = APIClient()
        response = client.get('/api/lessons/')
        print(f"UNAUTHENTICATED RESPONSE: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_with_auth(self):
        """Тест доступа с аутентификацией"""
        client = APIClient()
        user = User.objects.create_user(
            email='auth@test.com',
            password='test123'
        )
        client.force_authenticate(user=user)

        response = client.get('/api/lessons/')
        print(f"AUTHENTICATED RESPONSE: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)