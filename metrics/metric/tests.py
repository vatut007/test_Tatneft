from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Metric


class MetricCreateTestCase(APITestCase):
    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.url = reverse('metric-list')
        self.valid_data = {
            'name': 'response_time',
            'value': 150.5,
            'unit': 'ms'
        }
        self.invalid_data = {
            'name': '',
            'value': -10,
            'unit': 'unknown'
        }

    def test_create_metric_success(self):
        """Тест успешного создания метрики"""
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['name'], self.valid_data['name'])
        self.assertEqual(float(response.data['value']), self.valid_data['value'])
        self.assertTrue(Metric.objects.filter(name=self.valid_data['name']).exists())
        metric = Metric.objects.get(name=self.valid_data['name'])
        self.assertEqual(metric.value, self.valid_data['value'])

    def test_create_metric_invalid_data(self):
        """Тест создания с некорректными данными"""
        response = self.client.post(self.url, self.invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('value', response.data)

    def test_create_metric_missing_required_fields(self):
        """Тест отсутствия обязательных полей"""
        incomplete_data = {'name': 'test_metric'}
        response = self.client.post(self.url, incomplete_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('value', response.data)  # value обязателен

    def test_create_metric_duplicate_name(self):
        """Тест попытки создать метрику с существующим именем"""
        Metric.objects.create(name='unique_metric', value=100, unit='ms')

        duplicate_data = {'name': 'unique_metric', 'value': 200, 'unit': 'ms'}
        response = self.client.post(self.url, duplicate_data, format='json')

        if Metric._meta.get_field('name').unique:  # если имя уникально
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('name', response.data)
        else:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_metric_unauthorized(self):
        """Тест без аутентификации (если требуется)"""
        from django.contrib.auth.models import User
        User.objects.create_user(username='testuser', password='testpass')
        self.client.logout()

        response = self.client.post(self.url, self.valid_data, format='json')
        # Если аутентификация обязательна — должен быть 401/403
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_create_metric_with_authentication(self):
        """Тест с аутентификацией"""
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)

        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
