from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Pessoa


class AuthenticationAPITest(APITestCase):
    """Test authentication endpoints"""
    
    def test_register_success(self):
        """Test successful user registration"""
        data = {
            'username': 'newuser',
            'password': 'SecurePass123!',
            'name': 'New User',
            'email': 'new@example.com',
            'phone': '+1234567890'
        }
        
        response = self.client.post('/api/auth/register/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('pessoa', response.data)
        self.assertEqual(response.data['pessoa']['name'], 'New User')
        
        # Verify user and pessoa were created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Pessoa.objects.filter(email='new@example.com').exists())
    
    def test_register_weak_password(self):
        """Test registration with weak password"""
        data = {
            'username': 'newuser',
            'password': '123',  # Too weak
            'name': 'New User',
            'email': 'new@example.com'
        }
        
        response = self.client.post('/api/auth/register/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_register_duplicate_username(self):
        """Test registration with existing username"""
        User.objects.create_user(username='existing', password='pass')
        
        data = {
            'username': 'existing',  # Duplicate
            'password': 'SecurePass123!',
            'name': 'New User',
            'email': 'new@example.com'
        }
        
        response = self.client.post('/api/auth/register/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_success(self):
        """Test successful login"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        Pessoa.objects.create(
            user=user,
            name='Test User',
            email='test@example.com'
        )
        
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post('/api/auth/login/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('pessoa', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with wrong password"""
        User.objects.create_user(username='testuser', password='correctpass')
        
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        
        response = self.client.post('/api/auth/login/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_logout(self):
        """Test logout"""
        user = User.objects.create_user(username='testuser', password='pass')
        Pessoa.objects.create(user=user, name='Test', email='test@example.com')
        
        # Login first
        login_response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'pass'
        })
        token = login_response.data['token']
        
        # Logout
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post('/api/auth/logout/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify token is deleted - subsequent requests should fail
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_profile(self):
        """Test getting user profile"""
        user = User.objects.create_user(username='testuser', password='pass')
        pessoa = Pessoa.objects.create(
            user=user,
            name='Test User',
            email='test@example.com',
            phone='+1234567890'
        )
        
        # Login
        login_response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'pass'
        })
        token = login_response.data['token']
        
        # Get profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get('/api/auth/profile/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test User')
        self.assertEqual(response.data['email'], 'test@example.com')
    
    def test_change_password(self):
        """Test password change"""
        user = User.objects.create_user(username='testuser', password='oldpass123')
        Pessoa.objects.create(user=user, name='Test', email='test@example.com')
        
        # Login
        login_response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'oldpass123'
        })
        token = login_response.data['token']
        
        # Change password
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post('/api/auth/change-password/', {
            'old_password': 'oldpass123',
            'new_password': 'NewSecurePass456!'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)  # New token returned
        
        # Verify can login with new password
        new_login = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'NewSecurePass456!'
        })
        self.assertEqual(new_login.status_code, status.HTTP_200_OK)
    
    def test_throttling(self):
        """Test authentication endpoint throttling"""
        # Attempt multiple login requests
        for i in range(6):  # Exceeds 5/minute limit
            self.client.post('/api/auth/login/', {
                'username': 'test',
                'password': 'test'
            })
        
        response = self.client.post('/api/auth/login/', {
            'username': 'test',
            'password': 'test'
        })
        
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)