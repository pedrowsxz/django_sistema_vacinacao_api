from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from core.models import Pet
from core.serializers import PetSerializer, PetDetailSerializer
from core.permissions import IsPessoaOrReadOnly


class PetViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD de Pets.
    
    list: Obter todos os pets (filtrados pela pessoa para usuários comuns)
    create: Registrar um novo pet
    retrieve: Obter detalhes do pet com histórico de vacinação
    update: Atualizar informações do pet
    destroy: Deletar um pet
    """
    permission_classes = [IsAuthenticated, IsPessoaOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'breed', 'pessoa__name']
    ordering_fields = ['name', 'birth_date', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Filtrar pets com base nas permissões do usuário.
        Usuários comuns só podem ver seus próprios pets.
        Staff pode ver todos os pets.
        """
        user = self.request.user
        queryset = Pet.objects.select_related('pessoa', 'pessoa__user')
        
        if user.is_staff:
            # Staff pode ver todos os pets
            queryset = queryset.all()
        else:
            # Usuários comuns só veem seus próprios pets
            queryset = queryset.filter(pessoa__user=user)
        
        # Filtrar por espécie, se fornecida
        species = self.request.query_params.get('species', None)
        if species:
            queryset = queryset.filter(species=species)
        
        # Filtrar por pessoa, se fornecido (útil para staff)
        pessoa_id = self.request.query_params.get('pessoa', None)
        if pessoa_id:
            queryset = queryset.filter(pessoa_id=pessoa_id)
        
        return queryset
    
    def get_serializer_class(self):
        """Use detailed serializer for retrieve action"""
        if self.action == 'retrieve':
            return PetDetailSerializer
        return PetSerializer
    
    def perform_create(self, serializer):
        """
        Automatically set pessoa from authenticated user.
        For staff users, allow specifying pessoa.
        """
        if not self.request.user.is_staff:
            # Usuários comuns: atribuir automaticamente ao perfil pessoa
            serializer.save(pessoa=self.request.user.pessoa)
        else:
            # Staff pode especificar a pessoa
            serializer.save()
    
    @action(detail=True, methods=['get'])
    def vaccinations(self, request, pk=None):
        """Obter todos os registros de vacinação de um pet específico"""
        pet = self.get_object()
        from core.serializers import VaccinationRecordSerializer
        records = pet.vaccination_records.select_related('vaccine').order_by('-administered_date')
        serializer = VaccinationRecordSerializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def upcoming_vaccinations(self, request, pk=None):
        """Obter vacinações futuras/próximas de um pet"""
        pet = self.get_object()
        from core.serializers import VaccinationRecordSerializer
        
        records = pet.vaccination_records.filter(
            next_dose_date__isnull=False
        ).select_related('vaccine').order_by('next_dose_date')
        
        due_soon = [r for r in records if r.is_due]
        overdue = [r for r in records if r.is_overdue]
        
        return Response({
            'due_soon': VaccinationRecordSerializer(due_soon, many=True).data,
            'overdue': VaccinationRecordSerializer(overdue, many=True).data
        })