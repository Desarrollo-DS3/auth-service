from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class UserRegistrationLoginTest(APITestCase):
    def test_user_registration(self):
        url = reverse('register_user')
        data2 = {
        'email': 'testuser2@example.com',
        'first_name': 'Test2',
        'last_name': 'User2',
        'password': 'Testpassword1234',
        'role': 'user'
    }
        response = self.client.post(url, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual({"message": "User registered successfully"}, response.data)

class UserLoginTest(APITestCase):
    data = {
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'Testpassword123',
        'role': 'user'
        }    
    def setUp(self):
        url = reverse('register_user')
        self.client.post(url, self.data, format='json')
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'Testpassword123'
        }

    def test_user_login(self):
        url = reverse('login')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

from django.contrib.auth import get_user_model

class WarehouseAssistantRegistrationTest(APITestCase):
    def setUp(self):
        '''        User = get_user_model()
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            first_name='admin',
            last_name='admin',
            password='Adminpassword123',
            role='admin'
        )
        self.client.login(email='admin@example.com', password='Adminpassword123')'''
    
        url = reverse('register_warehouse_assistant')
        data = {
            'email': 'assistant@example.com',
            'first_name': 'assitant',
            'last_name': 'warehouse',
            'password': 'Assistantpassword123',
            'role': 'warehouse_assistant'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Warehouse Assistant registered successfully')
