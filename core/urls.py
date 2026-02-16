from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    PessoaViewSet,
    PetViewSet,
    VaccineViewSet,
    VaccinationRecordViewSet,
)
from core.views.auth import register, login, logout, profile, update_profile, change_password 

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
    path('auth/profile/', profile, name='profile'),
    path('auth/profile/update/', update_profile, name='update-profile'),
    path('auth/change-password/', change_password, name='change-password'),
    
    # Router URLs (CRUD endpoints)
    path('', include(router.urls)),
]