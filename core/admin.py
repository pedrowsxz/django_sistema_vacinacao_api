from django.contrib import admin
from core.models import Pessoa, Pet, Vaccine, VaccinationRecord


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'total_pets', 'created_at']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'name', 'email', 'phone', 'address')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'breed', 'pessoa', 'birth_date', 'age_years', 'created_at']
    search_fields = ['name', 'pessoa__name']
    list_filter = ['species', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'age_years', 'age_months']
    autocomplete_fields = ['pessoa']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('pessoa', 'name', 'species', 'breed')
        }),
        ('Physical Details', {
            'fields': ('birth_date', 'age_years', 'age_months', 'color', 'weight')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ['name', 'manufacturer', 'species_target', 'duration_months', 'is_mandatory', 'created_at']
    search_fields = ['name', 'manufacturer']
    list_filter = ['is_mandatory', 'species_target', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Vaccine Information', {
            'fields': ('name', 'manufacturer', 'description', 'species_target')
        }),
        ('Scheduling', {
            'fields': ('duration_months', 'is_mandatory')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = [
        'pet', 'vaccine', 'administered_date', 'next_dose_date',
        'veterinarian_name', 'is_due', 'is_overdue'
    ]
    search_fields = ['pet__name', 'vaccine__name', 'veterinarian_name', 'clinic_name']
    list_filter = ['administered_date', 'vaccine', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'is_due', 'is_overdue', 'days_until_due']
    autocomplete_fields = ['pet', 'vaccine']
    date_hierarchy = 'administered_date'
    
    fieldsets = (
        ('Vaccination Details', {
            'fields': ('pet', 'vaccine', 'administered_date')
        }),
        ('Provider Information', {
            'fields': ('veterinarian_name', 'clinic_name', 'batch_number')
        }),
        ('Scheduling', {
            'fields': ('next_dose_date', 'is_due', 'is_overdue', 'days_until_due')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_due(self, obj):
        return obj.is_due
    is_due.boolean = True
    is_due.short_description = 'Due Soon'
    
    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'