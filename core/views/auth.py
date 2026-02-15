from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from core.serializers import PessoaCreateSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user and pessoa account.
    Returns the auth token and pessoa details.
    """
    serializer = PessoaCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        pessoa = serializer.save()
        token, created = Token.objects.get_or_create(user=pessoa.user)
        
        return Response({
            'token': token.key,
            'pessoa': {
                'id': pessoa.id,
                'username': pessoa.user.username,
                'name': pessoa.name,
                'email': pessoa.email
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Login with username and password.
    Returns the auth token and pessoa details.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Please provide both username and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    token, created = Token.objects.get_or_create(user=user)
    
    try:
        pessoa = user.pessoa
        pessoa_data = {
            'id': pessoa.id,
            'username': user.username,
            'name': pessoa.name,
            'email': pessoa.email
        }
    except:
        pessoa_data = None
    
    return Response({
        'token': token.key,
        'pessoa': pessoa_data
    })


@api_view(['POST'])
def logout(request):
    """
    Logout by deleting the auth token.
    """
    try:
        request.user.auth_token.delete()
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)
    except:
        return Response({
            'error': 'Something went wrong'
        }, status=status.HTTP_400_BAD_REQUEST)