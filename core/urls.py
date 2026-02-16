from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    PessoaViewSet,
    PetViewSet,
    VaccineViewSet,
    VaccinationRecordViewSet,
)
from core.views.auth import register, login, logout, profile, update_profile, change_password 

# Definir as rotas e registrar os viewsets
router = DefaultRouter()
router.register(r'pessoas', PessoaViewSet, basename='pessoa')
router.register(r'pets', PetViewSet, basename='pet')
router.register(r'vaccines', VaccineViewSet, basename='vaccine')
router.register(r'vaccinations', VaccinationRecordViewSet, basename='vaccination')

# Padrão de URL para a API
urlpatterns = [
    # Endpoints de autenticação
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    path('auth/profile/', profile, name='profile'),
    path('auth/profile/update/', update_profile, name='update-profile'),
    path('auth/change-password/', change_password, name='change-password'),
    
    # URLs das rotas (CRUD endpoints)
    path('', include(router.urls)),
]