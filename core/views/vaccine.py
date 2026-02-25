from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import Vaccine
from core.serializers import VaccineSerializer, VaccineDetailSerializer
from core.permissions import IsAdminOrReadOnly


class VaccineViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD de Vacinas.
    
    Apenas administradores podem criar/atualizar/deletar vacinas.
    Usuários comuns podem apenas ler informações sobre vacinas.

    """
    queryset = Vaccine.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'manufacturer', 'species_target']
    ordering_fields = ['name', 'duration_months', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Apply filters from query parameters"""
        queryset = super().get_queryset()
        
        # Filtrar por espécie
        species = self.request.query_params.get('species', None)
        if species:
            queryset = queryset.filter(species_target=species)
        
        # Filtrar por obrigatoriedade
        mandatory = self.request.query_params.get('mandatory', None)
        if mandatory is not None:
            is_mandatory = mandatory.lower() in ('true', '1', 'yes')
            queryset = queryset.filter(is_mandatory=is_mandatory)
        
        return queryset
    
    def get_serializer_class(self):
        """Usar serializer detalhado para retrieve"""
        if self.action == 'retrieve':
            return VaccineDetailSerializer
        return VaccineSerializer
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Obter estatísticas para uma vacina específica"""
        vaccine = self.get_object()
        
        total_administrations = vaccine.vaccination_records.count()
        
        # Obter estatísticas para uma vacina específica
        from django.db.models import Count
        by_species = vaccine.vaccination_records.values(
            'pet__species'
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Administrações recentes (últimos 30 dias)
        from datetime import date, timedelta
        thirty_days_ago = date.today() - timedelta(days=30)
        recent_count = vaccine.vaccination_records.filter(
            administered_date__gte=thirty_days_ago
        ).count()
        
        return Response({
            'vaccine': vaccine.name,
            'total_administrations': total_administrations,
            'recent_administrations_30d': recent_count,
            'by_species': list(by_species),
            'duration_months': vaccine.duration_months,
            'is_mandatory': vaccine.is_mandatory
        })