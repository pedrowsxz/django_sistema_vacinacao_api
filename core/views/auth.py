from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.throttling import AnonRateThrottle
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from core.serializers import PessoaCreateSerializer, PessoaSerializer


class AuthRateThrottle(AnonRateThrottle):
    """Throttle personalizado para endpoints de autenticação"""
    rate = '5/minute'


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
def register(request):
    """
    Registrar um novo usuário e conta de pessoa.
    
    Campos obrigatórios:
    - username: Nome de usuário único
    - password: Senha forte
    - name: Nome completo
    - email: Endereço de e-mail válido
    
    Campos opcionais:
    - phone: Número de contato
    - address: Endereço físico
    
    Retorna:
    - token: Token de autenticação
    - pessoa: Dados do perfil da pessoa
    """
    serializer = PessoaCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        # Validar força da senha
        password = request.data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({
                'password': list(e.messages)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create pessoa (também usuário)
        pessoa = serializer.save()
        
        # Gerar token de autenticação
        token, created = Token.objects.get_or_create(user=pessoa.user)
        
        return Response({
            'message': 'Registration successful',
            'token': token.key,
            'pessoa': {
                'id': pessoa.id,
                'username': pessoa.user.username,
                'name': pessoa.name,
                'email': pessoa.email,
                'phone': pessoa.phone
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
def login(request):
    """
    Autenticar usuário e retornar token.
    
    Campos obrigatórios:
    - username: Nome de usuário
    - password: Senha
    
    Retorna:
    - token: Token de autenticação
    - pessoa: Dados do perfil da pessoa (se existir)
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Validar o input
    if not username or not password:
        return Response({
            'error': 'Por favor, forneça tanto nome de usuário quanto senha'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Authenticação
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response({
            'error': 'Credenciais inválidas'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_active:
        return Response({
            'error': 'Conta desativada'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Get ou criar token de autenticação
    token, created = Token.objects.get_or_create(user=user)
    
    # Get perfil da pessoa se existe
    try:
        pessoa = user.pessoa
        pessoa_data = {
            'id': pessoa.id,
            'username': user.username,
            'name': pessoa.name,
            'email': pessoa.email,
            'phone': pessoa.phone
        }
    except:
        pessoa_data = {
            'username': user.username,
            'is_staff': user.is_staff
        }
    
    return Response({
        'message': 'Login successful',
        'token': token.key,
        'pessoa': pessoa_data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout do usuário deletando seu token de autenticação.
    Requer: Header Authorization com o token
    """
    try:
        # Deletar o token
        request.user.auth_token.delete()
        return Response({
            'message': 'Logout realizado com sucesso'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Ocorreu um erro durante o logout'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Obter informações do perfil do usuário atual.
    """
    try:
        pessoa = request.user.pessoa
        serializer = PessoaSerializer(pessoa)
        return Response(serializer.data)
    except:
        return Response({
            'error': 'Perfil de pessoa não encontrado para este usuário'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Atualizar informações do perfil do usuário atual.
    """
    try:
        pessoa = request.user.pessoa
        serializer = PessoaSerializer(pessoa, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Perfil atualizado com sucesso',
                'pessoa': serializer.data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({
            'error': 'Perfil de pessoa não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Alterar a senha do usuário.
    """
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response({
            'error': 'Por favor, forneça a senha antiga e a nova'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Checa a senha antiga
    if not user.check_password(old_password):
        return Response({
            'error': 'Senha antiga está incorreta'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Valida a nova senha
    try:
        validate_password(new_password, user)
    except ValidationError as e:
        return Response({
            'new_password': list(e.messages)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Seta a nova senha
    user.set_password(new_password)
    user.save()
    
    # Deleta o token antigo e cria um novo
    Token.objects.filter(user=user).delete()
    token = Token.objects.create(user=user)
    
    return Response({
        'message': 'Senha alterada com sucesso',
        'token': token.key
    })