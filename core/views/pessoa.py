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
    ViewSet para operações CRUD de Pessoa.
    
    list: Obter todas as pessoas (somente admin) ou perfil da pessoa do usuário atual
    create: Registrar uma nova pessoa com conta de usuário
    retrieve: Obter detalhes da pessoa com lista de pets
    update: Atualizar informações da pessoa
    destroy: Deletar conta da pessoa
    """
    permission_classes = [IsAuthenticated, IsPessoa]
    
    def get_queryset(self):
        """
        Filtrar queryset com base nas permissões do usuário.
        Usuários comuns só podem ver seu próprio perfil de pessoa.
        Staff/admin pode ver todas as pessoas.
        """
        user = self.request.user
        if user.is_staff:
            return Pessoa.objects.annotate(
                pet_count=Count('pets')
            ).select_related('user').all()
        
        # Usuários comuns só podem acessar seu próprio perfil de pessoa
        return Pessoa.objects.filter(user=user).annotate(
            pet_count=Count('pets')
        )
    
    def get_serializer_class(self):
        """Usar serializers diferentes para ações diferentes"""
        if self.action == 'create':
            return PessoaCreateSerializer
        elif self.action == 'retrieve':
            return PessoaDetailSerializer
        return PessoaSerializer
    
    def get_permissions(self):
        """Permitir que qualquer pessoa crie uma conta (registro)"""
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
    
    @action(detail=True, methods=['get'])
    def pets(self, request, pk=None):
        """Obter todos os pets de uma pessoa específica"""
        pessoa = self.get_object()
        from core.serializers import PetSerializer
        pets = pessoa.pets.all()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def vaccination_summary(self, request, pk=None):
        """Obter resumo de vacinação de todos os pets da pessoa"""
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