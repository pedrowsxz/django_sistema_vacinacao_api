from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import date, timedelta
from core.models import VaccinationRecord
from core.serializers import (
    VaccinationRecordSerializer,
    VaccinationRecordDetailSerializer
)
from core.permissions import IsPessoaOrReadOnly


class VaccinationRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD de Registro de Vacinação.
    
    list: Obter todos os registros de vacinação (filtrados pelo proprietário)
    create: Registrar uma nova vacinação
    retrieve: Obter registro de vacinação detalhado
    update: Atualizar registro de vacinação
    destroy: Deletar um registro de vacinação
    """
    permission_classes = [IsAuthenticated, IsPessoaOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['pet__name', 'vaccine__name', 'veterinarian_name', 'clinic_name']
    ordering_fields = ['administered_date', 'next_dose_date', 'created_at']
    ordering = ['-administered_date']
    
    def get_queryset(self):
        """
        Filtrar registros de vacinação com base nas permissões do usuário.
        Usuários comuns só podem ver registros dos seus próprios pets.
        """
        user = self.request.user
        queryset = VaccinationRecord.objects.select_related(
            'pet', 'pet__pessoa', 'vaccine'
        )
        
        if user.is_staff:
            queryset = queryset.all()
        else:
            # Filtrar apenas registros dos pets do usuário
            queryset = queryset.filter(pet__pessoa__user=user)
        
        # Filtrar por pet
        pet_id = self.request.query_params.get('pet', None)
        if pet_id:
            queryset = queryset.filter(pet_id=pet_id)
        
        # Filtrar por vacina
        vaccine_id = self.request.query_params.get('vaccine', None)
        if vaccine_id:
            queryset = queryset.filter(vaccine_id=vaccine_id)
        
        # Filtrar por intervalo de datas
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if date_from:
            queryset = queryset.filter(administered_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(administered_date__lte=date_to)
        
        return queryset
    
    def get_serializer_class(self):
        """Usar serializer detalhado para a ação retrieve"""
        if self.action == 'retrieve':
            return VaccinationRecordDetailSerializer
        return VaccinationRecordSerializer
    
    def perform_create(self, serializer):
        """
        Atribuir o pet ao usuário autenticado ao criar um registro de vacinação.
        """
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def due_soon(self, request):
        """Obter todas as vacinações com data de próxima dose nos próximos 30 dias"""
        user = request.user
        today = date.today()
        thirty_days = today + timedelta(days=30)
        
        queryset = self.get_queryset().filter(
            next_dose_date__gte=today,
            next_dose_date__lte=thirty_days
        ).order_by('next_dose_date')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Obter todas as vacinações atrasadas"""
        today = date.today()
        
        queryset = self.get_queryset().filter(
            next_dose_date__lt=today
        ).order_by('next_dose_date')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Obter vacinações recentes (últimos 30 dias)"""
        thirty_days_ago = date.today() - timedelta(days=30)
        
        queryset = self.get_queryset().filter(
            administered_date__gte=thirty_days_ago
        ).order_by('-administered_date')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)