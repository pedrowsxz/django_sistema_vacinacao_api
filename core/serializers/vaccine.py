from rest_framework import serializers
from core.models import Vaccine


class VaccineSerializer(serializers.ModelSerializer):
    """
    Standard serializer for Vaccine operations.
    """
    total_administrations = serializers.SerializerMethodField()
    
    class Meta:
        model = Vaccine
        fields = [
            'id',
            'name',
            'manufacturer',
            'description',
            'species_target',
            'duration_months',
            'is_mandatory',
            'total_administrations',
            'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_total_administrations(self, obj):
        """Count how many times this vaccine has been administered"""
        return obj.vaccination_records.count()
    
    def validate_duration_months(self, value):
        """Ensure duration is positive"""
        if value < 1:
            raise serializers.ValidationError("Duration must be at least 1 month.")
        return value


class VaccineDetailSerializer(VaccineSerializer):
    """
    Detailed serializer with recent administrations.
    """
    recent_administrations = serializers.SerializerMethodField()
    
    class Meta(VaccineSerializer.Meta):
        fields = VaccineSerializer.Meta.fields + ['recent_administrations', 'updated_at']
    
    def get_recent_administrations(self, obj):
        """Return recent vaccination records using this vaccine"""
        from core.serializers.vaccination_record import VaccinationRecordMinimalSerializer
        records = obj.vaccination_records.select_related('pet', 'pet__pessoa').order_by('-administered_date')[:5]
        return VaccinationRecordMinimalSerializer(records, many=True).data