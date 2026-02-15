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
    ViewSet for VaccinationRecord CRUD operations.
    
    list: Get all vaccination records (filtered by owner)
    create: Record a new vaccination
    retrieve: Get detailed vaccination record
    update: Update vaccination record
    destroy: Delete a vaccination record
    """
    permission_classes = [IsAuthenticated, IsPessoaOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['pet__name', 'vaccine__name', 'veterinarian_name', 'clinic_name']
    ordering_fields = ['administered_date', 'next_dose_date', 'created_at']
    ordering = ['-administered_date']
    
    def get_queryset(self):
        """
        Filter vaccination records based on user permissions.
        Regular users can only see records for their own pets.
        """
        user = self.request.user
        queryset = VaccinationRecord.objects.select_related(
            'pet', 'pet__pessoa', 'vaccine'
        )
        
        if user.is_staff:
            queryset = queryset.all()
        else:
            # Filter to only show records for user's pets
            queryset = queryset.filter(pet__pessoa__user=user)
        
        # Filter by pet
        pet_id = self.request.query_params.get('pet', None)
        if pet_id:
            queryset = queryset.filter(pet_id=pet_id)
        
        # Filter by vaccine
        vaccine_id = self.request.query_params.get('vaccine', None)
        if vaccine_id:
            queryset = queryset.filter(vaccine_id=vaccine_id)
        
        # Filter by date range
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if date_from:
            queryset = queryset.filter(administered_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(administered_date__lte=date_to)
        
        return queryset
    
    def get_serializer_class(self):
        """Use detailed serializer for retrieve action"""
        if self.action == 'retrieve':
            return VaccinationRecordDetailSerializer
        return VaccinationRecordSerializer
    
    def perform_create(self, serializer):
        """
        Validate pet ownership before creating record.
        Regular users can only create records for their own pets.
        """
        pet = serializer.validated_data.get('pet')
        
        if not self.request.user.is_staff:
            # Verify the pet belongs to the current user
            if pet.pessoa.user != self.request.user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You can only add vaccination records for your own pets.")
        
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def due_soon(self, request):
        """Get all vaccinations due within the next 30 days"""
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
        """Get all overdue vaccinations"""
        today = date.today()
        
        queryset = self.get_queryset().filter(
            next_dose_date__lt=today
        ).order_by('next_dose_date')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent vaccinations (last 30 days)"""
        thirty_days_ago = date.today() - timedelta(days=30)
        
        queryset = self.get_queryset().filter(
            administered_date__gte=thirty_days_ago
        ).order_by('-administered_date')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)