from rest_framework import status
from core.tests import BaseAPITestCase
from core.models import Pet, Vaccine, VaccinationRecord
from datetime import date


class PermissionTest(BaseAPITestCase):
    """Test permission controls across all endpoints"""
    
    def setUp(self):
        super().setUp()
        
        # Create test data
        self.pet1 = Pet.objects.create(
            pessoa=self.pessoa1,
            name='Rex',
            species='dog',
            birth_date=date(2020, 1, 1)
        )
        self.pet2 = Pet.objects.create(
            pessoa=self.pessoa2,
            name='Max',
            species='dog',
            birth_date=date(2019, 1, 1)
        )
        
        self.vaccine = Vaccine.objects.create(
            name='Rabies',
            duration_months=12
        )
        
        self.record1 = VaccinationRecord.objects.create(
            pet=self.pet1,
            vaccine=self.vaccine,
            administered_date=date(2024, 1, 15),
            veterinarian_name='Dr. Smith'
        )
        self.record2 = VaccinationRecord.objects.create(
            pet=self.pet2,
            vaccine=self.vaccine,
            administered_date=date(2024, 1, 20),
            veterinarian_name='Dr. Jones'
        )
    
    def test_user_cannot_view_other_user_pets(self):
        """Test that user1 cannot see user2's pets in list"""
        self.authenticate_user1()
        
        response = self.client.get('/api/pets/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that only user1's pets are returned
        pet_ids = [pet['id'] for pet in response.data['results']]
        self.assertIn(self.pet1.id, pet_ids)
        self.assertNotIn(self.pet2.id, pet_ids)
    
    def test_user_cannot_update_other_user_pet(self):
        """Test that user1 cannot update user2's pet"""
        self.authenticate_user1()
        
        data = {'name': 'Hacked Name'}
        response = self.client.patch(f'/api/pets/{self.pet2.id}/', data, format='json')
        
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
    
    def test_user_cannot_delete_other_user_pet(self):
        """Test that user1 cannot delete user2's pet"""
        self.authenticate_user1()
        
        response = self.client.delete(f'/api/pets/{self.pet2.id}/')
        
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
        
        # Verify pet still exists
        self.assertTrue(Pet.objects.filter(id=self.pet2.id).exists())
    
    def test_user_cannot_view_other_user_vaccination_records(self):
        """Test that vaccination records are filtered by pessoaship"""
        self.authenticate_user1()
        
        response = self.client.get('/api/vaccinations/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that only user1's records are returned
        record_ids = [rec['id'] for rec in response.data['results']]
        self.assertIn(self.record1.id, record_ids)
        self.assertNotIn(self.record2.id, record_ids)
    
    def test_user_cannot_update_other_user_vaccination_record(self):
        """Test that user cannot update another user's vaccination record"""
        self.authenticate_user1()
        
        data = {'notes': 'Hacked notes'}
        response = self.client.patch(
            f'/api/vaccinations/{self.record2.id}/',
            data,
            format='json'
        )
        
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
    
    def test_user_can_update_own_pet(self):
        """Test that user can update their own pet"""
        self.authenticate_user1()
        
        data = {'name': 'Rex Updated'}
        response = self.client.patch(f'/api/pets/{self.pet1.id}/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Rex Updated')
    
    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated users cannot access endpoints"""
        endpoints = [
            '/api/pets/',
            '/api/vaccines/',
            '/api/vaccinations/',
            '/api/pessoas/'
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                f"Endpoint {endpoint} should require authentication"
            )
    
    def test_pessoa_profile_access_control(self):
        """Test that users can only access their own pessoa profile"""
        self.authenticate_user1()
        
        # Can access own profile
        response = self.client.get(f'/api/pessoas/{self.pessoa1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Cannot access other profile
        response = self.client.get(f'/api/pessoas/{self.pessoa2.id}/')
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])