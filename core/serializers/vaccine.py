from rest_framework import serializers
from core.models import Vaccine


class VaccineSerializer(serializers.ModelSerializer):
    """
    Serializer padrão para operações com Vaccine.
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
        """Contar quantas vezes esta vacina foi administrada"""
        return obj.vaccination_records.count()
    
    def validate_duration_months(self, value):
        """Garantir que a duração seja positiva"""
        if value < 1:
            raise serializers.ValidationError("A duração deve ser pelo menos 1 mês.")
        return value


class VaccineDetailSerializer(VaccineSerializer):
    """
    Serializer detalhado com administrações recentes.
    """
    recent_administrations = serializers.SerializerMethodField()
    
    class Meta(VaccineSerializer.Meta):
        fields = VaccineSerializer.Meta.fields + ['recent_administrations', 'updated_at']
    
    def get_recent_administrations(self, obj):
        """Retornar registros recentes de vacinação usando esta vacina"""
        from core.serializers.vaccination_record import VaccinationRecordMinimalSerializer
        records = obj.vaccination_records.select_related('pet', 'pet__pessoa').order_by('-administered_date')[:5]
        return VaccinationRecordMinimalSerializer(records, many=True).data