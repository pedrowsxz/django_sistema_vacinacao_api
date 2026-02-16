from rest_framework import serializers
from core.models import Pet
from datetime import date


class PetMinimalSerializer(serializers.ModelSerializer):
    """
    Dados mínimos do pet para representações aninhadas.
    """
    species_display = serializers.CharField(source='get_species_display', read_only=True)
    age_years = serializers.ReadOnlyField()
    
    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'species_display', 'breed', 'age_years']


class PetSerializer(serializers.ModelSerializer):
    """
    Serializer para listagem e criação de Pet.
    """
    pessoa_name = serializers.CharField(source='pessoa.name', read_only=True)
    species_display = serializers.CharField(source='get_species_display', read_only=True)
    age_years = serializers.ReadOnlyField()
    age_months = serializers.ReadOnlyField()
    
    class Meta:
        model = Pet
        fields = [
            'id',
            'pessoa',
            'pessoa_name',
            'name',
            'species',
            'species_display',
            'breed',
            'birth_date',
            'age_years',
            'age_months',
            'color',
            'weight',
            'notes',
            'created_at'
        ]
        read_only_fields = ['created_at']
    
    def validate_birth_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("A data de nascimento não pode estar no futuro.")
        return value
    
    def validate_weight(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("O peso deve ser maior que zero.")
        return value


class PetDetailSerializer(PetSerializer):
    """
    Serializer detalhado com histórico de vacinação.
    """
    pessoa = serializers.SerializerMethodField()
    vaccination_history = serializers.SerializerMethodField()
    vaccination_count = serializers.SerializerMethodField()
    
    class Meta(PetSerializer.Meta):
        fields = PetSerializer.Meta.fields + [
            'vaccination_history',
            'vaccination_count',
            'updated_at'
        ]
    
    def get_pessoa(self, obj):
        """Retornar detalhes da pessoa"""
        return {
            'id': obj.pessoa.id,
            'name': obj.pessoa.name,
            'email': obj.pessoa.email,
            'phone': obj.pessoa.phone
        }
    
    def get_vaccination_history(self, obj):
        """Retornar registros de vacinação deste pet"""
        from core.serializers.vaccination_record import VaccinationRecordSerializer
        records = obj.vaccination_records.select_related('vaccine').order_by('-administered_date')[:10]
        return VaccinationRecordSerializer(records, many=True).data
    
    def get_vaccination_count(self, obj):
        """Retornar contagem total de vacinações"""
        return obj.vaccination_records.count()