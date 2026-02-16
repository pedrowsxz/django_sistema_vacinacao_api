from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count
from core.models import Pessoa
from core.serializers import (
    PessoaSerializer,
    PessoaDetailSerializer,
    PessoaCreateSerializer
)
from core.permissions import IsPessoa, IsPessoaOrReadOnly


class PessoaViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Pessoa CRUD operations.
    
    list: Get all pessoas (admin only) or current user's pessoa profile
    create: Register a new pessoa with user account
    retrieve: Get pessoa details with pet list
    update: Update pessoa information
    destroy: Delete pessoa account
    """
    # FIXED: Use IsPessoa for stricter permission control
    permission_classes = [IsAuthenticated, IsPessoa]
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions.
        Regular users can only see their own pessoa profile.
        Staff can see all pessoas.
        """
        user = self.request.user
        if user.is_staff:
            return Pessoa.objects.annotate(
                pet_count=Count('pets')
            ).select_related('user').all()
        
        # Regular users can only access their own pessoa profile
        return Pessoa.objects.filter(user=user).annotate(
            pet_count=Count('pets')
        )
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'create':
            return PessoaCreateSerializer
        elif self.action == 'retrieve':
            return PessoaDetailSerializer
        return PessoaSerializer
    
    def get_permissions(self):
        """Allow anyone to create an account (register)"""
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
    
    @action(detail=True, methods=['get'])
    def pets(self, request, pk=None):
        """Get all pets for a specific pessoa"""
        pessoa = self.get_object()
        from core.serializers import PetSerializer
        pets = pessoa.pets.all()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def vaccination_summary(self, request, pk=None):
        """Get vaccination summary for all pessoa's pets"""
        pessoa = self.get_object()
        
        summary = {
            'total_pets': pessoa.pets.count(),
            'total_vaccinations': 0,
            'due_soon': 0,
            'overdue': 0,
            'pets': []
        }
        
        for pet in pessoa.pets.all():
            pet_data = {
                'id': pet.id,
                'name': pet.name,
                'species': pet.species,
                'total_vaccinations': pet.vaccination_records.count(),
                'due_vaccinations': [],
                'overdue_vaccinations': []
            }
            
            for record in pet.vaccination_records.all():
                summary['total_vaccinations'] += 1
                
                if record.is_due:
                    summary['due_soon'] += 1
                    pet_data['due_vaccinations'].append({
                        'vaccine': record.vaccine.name,
                        'next_dose_date': record.next_dose_date,
                        'days_until_due': record.days_until_due
                    })
                
                if record.is_overdue:
                    summary['overdue'] += 1
                    pet_data['overdue_vaccinations'].append({
                        'vaccine': record.vaccine.name,
                        'next_dose_date': record.next_dose_date,
                        'days_overdue': abs(record.days_until_due)
                    })
            
            summary['pets'].append(pet_data)
        
        return Response(summary)