from rest_framework import serializers
from core.models import VaccinationRecord
from datetime import date


class VaccinationRecordMinimalSerializer(serializers.ModelSerializer):
    """
    Minimal vaccination record for nested representations.
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
    Standard serializer for VaccinationRecord operations.
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
        """Ensure administered date is not in the future"""
        if value > date.today():
            raise serializers.ValidationError("Vaccination date cannot be in the future.")
        return value
    
    def validate(self, data):
        """
        Cross-field validation:
        - Ensure vaccination date is after pet's birth date
        """
        pet = data.get('pet')
        administered_date = data.get('administered_date')
        
        if pet and administered_date:
            if administered_date < pet.birth_date:
                raise serializers.ValidationError({
                    'administered_date': "Vaccination date cannot be before pet's birth date."
                })
        
        return data


class VaccinationRecordDetailSerializer(VaccinationRecordSerializer):
    """
    Detailed serializer with full pet and vaccine information.
    """
    pet = serializers.SerializerMethodField()
    vaccine = serializers.SerializerMethodField()
    
    class Meta(VaccinationRecordSerializer.Meta):
        fields = VaccinationRecordSerializer.Meta.fields + ['updated_at']
    
    def get_pet(self, obj):
        """Return pet details"""
        return {
            'id': obj.pet.id,
            'name': obj.pet.name,
            'species': obj.pet.species,
            'breed': obj.pet.breed,
            'pessoa_name': obj.pet.pessoa.name
        }
    
    def get_vaccine(self, obj):
        """Return vaccine details"""
        return {
            'id': obj.vaccine.id,
            'name': obj.vaccine.name,
            'manufacturer': obj.vaccine.manufacturer,
            'duration_months': obj.vaccine.duration_months,
            'is_mandatory': obj.vaccine.is_mandatory
        }