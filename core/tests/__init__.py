from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core.models import Pessoa, Pet, Vaccine, VaccinationRecord
from datetime import date, timedelta


class BaseTestCase(TestCase):
    """Base test case with common setup"""
    
    def setUp(self):
        """Create base test data"""
        # Create users
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123',
            email='user1@test.com'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123',
            email='user2@test.com'
        )
        
        # Create pessoas
        self.pessoa1 = Pessoa.objects.create(
            user=self.user1,
            name='Pessoa One',
            email='pessoa1@test.com',
            phone='+1234567890'
        )
        self.pessoa2 = Pessoa.objects.create(
            user=self.user2,
            name='Pessoa Two',
            email='pessoa2@test.com',
            phone='+0987654321'
        )


class BaseAPITestCase(APITestCase):
    """Base API test case with authentication"""
    
    def setUp(self):
        """Create base test data and setup API client"""
        self.client = APIClient()
        
        # Create users
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123',
            email='user1@test.com'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123',
            email='user2@test.com'
        )
        
        # Create pessoas
        self.pessoa1 = Pessoa.objects.create(
            user=self.user1,
            name='Pessoa One',
            email='pessoa1@test.com',
            phone='+1234567890'
        )
        self.pessoa2 = Pessoa.objects.create(
            user=self.user2,
            name='Pessoa Two',
            email='pessoa2@test.com',
            phone='+0987654321'
        )
        
        # Create tokens
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
    
    def authenticate_user1(self):
        """Authenticate as user1"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
    
    def authenticate_user2(self):
        """Authenticate as user2"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
    
    def clear_authentication(self):
        """Remove authentication"""
        self.client.credentials()