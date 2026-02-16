from rest_framework import serializers
from core.models import VaccinationRecord
from datetime import date


class VaccinationRecordMinimalSerializer(serializers.ModelSerializer):
    """
    Registro de vacinação para representações aninhadas.
    """
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    vaccine_name = serializers.CharField(source='vaccine.name', read_only=True)
    
    class Meta:
        model = VaccinationRecord
        fields = [
            'id',
            'pet_name',
            'vaccine_name',
            'administered_date',
            'next_dose_date'
        ]


class VaccinationRecordSerializer(serializers.ModelSerializer):
    """
    Serializer padrão para operações de VaccinationRecord.
    """
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    vaccine_name = serializers.CharField(source='vaccine.name', read_only=True)
    is_due = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    days_until_due = serializers.ReadOnlyField()
    
    class Meta:
        model = VaccinationRecord
        fields = [
            'id',
            'pet',
            'pet_name',
            'vaccine',
            'vaccine_name',
            'administered_date',
            'veterinarian_name',
            'clinic_name',
            'batch_number',
            'next_dose_date',
            'is_due',
            'is_overdue',
            'days_until_due',
            'notes',
            'created_at'
        ]
        read_only_fields = ['created_at', 'next_dose_date']
    
    def validate_administered_date(self, value):
        """Garantir que a data de vacinação não seja futura"""
        if value > date.today():
            raise serializers.ValidationError("A data da vacinação não pode estar no futuro.")
        return value
    
    def validate(self, data):
        """
        Validação cruzada entre campos:
        - Garantir que a data da vacinação seja após a data de nascimento do pet
        """
        pet = data.get('pet')
        administered_date = data.get('administered_date')
        
        if pet and administered_date:
            if administered_date < pet.birth_date:
                raise serializers.ValidationError({
                    'administered_date': "A data da vacinação não pode ser anterior à data de nascimento do pet."
                })
        
        return data


class VaccinationRecordDetailSerializer(VaccinationRecordSerializer):
    """
    Serializer detalhado com informações completas do pet e da vacina.
    """
    pet = serializers.SerializerMethodField()
    vaccine = serializers.SerializerMethodField()
    
    class Meta(VaccinationRecordSerializer.Meta):
        fields = VaccinationRecordSerializer.Meta.fields + ['updated_at']
    
    def get_pet(self, obj):
        """Retornar detalhes do pet"""
        return {
            'id': obj.pet.id,
            'name': obj.pet.name,
            'species': obj.pet.species,
            'breed': obj.pet.breed,
            'pessoa_name': obj.pet.pessoa.name
        }
    
    def get_vaccine(self, obj):
        """Retornar detalhes da vacina"""
        return {
            'id': obj.vaccine.id,
            'name': obj.vaccine.name,
            'manufacturer': obj.vaccine.manufacturer,
            'duration_months': obj.vaccine.duration_months,
            'is_mandatory': obj.vaccine.is_mandatory
        }