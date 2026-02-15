from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    PessoaViewSet,
    PetViewSet,
    VaccineViewSet,
    VaccinationRecordViewSet,
    register,
    login,
    logout
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'pessoas', PessoaViewSet, basename='pessoa')
router.register(r'pets', PetViewSet, basename='pet')
router.register(r'vaccines', VaccineViewSet, basename='vaccine')
router.register(r'vaccinations', VaccinationRecordViewSet, basename='vaccination')

# URL patterns
urlpatterns = [
    # Authentication endpoints
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    
    # Router URLs (CRUD endpoints)
    path('', include(router.urls)),
]