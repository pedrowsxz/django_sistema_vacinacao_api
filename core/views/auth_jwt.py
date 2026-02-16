from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from core.serializers import PessoaCreateSerializer, PessoaSerializer


class AuthRateThrottle(AnonRateThrottle):
    rate = '5/minute'


def get_tokens_for_user(user):
    """Generate JWT tokens for user"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
def register(request):
    """Register new user with JWT tokens"""
    serializer = PessoaCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        password = request.data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({
                'password': list(e.messages)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        pessoa = serializer.save()
        tokens = get_tokens_for_user(pessoa.user)
        
        return Response({
            'message': 'Registration successful',
            'tokens': tokens,
            'pessoa': {
                'id': pessoa.id,
                'username': pessoa.user.username,
                'name': pessoa.name,
                'email': pessoa.email,
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
def login(request):
    """Login with JWT tokens"""
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
    
    if not user.is_active:
        return Response({
            'error': 'Account is disabled'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    tokens = get_tokens_for_user(user)
    
    try:
        pessoa = user.pessoa
        pessoa_data = {
            'id': pessoa.id,
            'username': user.username,
            'name': pessoa.name,
            'email': pessoa.email,
        }
    except:
        pessoa_data = {'username': user.username, 'is_staff': user.is_staff}
    
    return Response({
        'message': 'Login successful',
        'tokens': tokens,
        'pessoa': pessoa_data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout by blacklisting the refresh token.
    Send refresh token in request body.
    """
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({
                'error': 'Refresh token required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Invalid token or token already blacklisted'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    Refresh access token using refresh token.
    Send refresh token in request body.
    """
    try:
        refresh = request.data.get('refresh')
        if not refresh:
            return Response({
                'error': 'Refresh token required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        refresh_token = RefreshToken(refresh)
        
        return Response({
            'access': str(refresh_token.access_token)
        })
    except Exception as e:
        return Response({
            'error': 'Invalid or expired refresh token'
        }, status=status.HTTP_401_UNAUTHORIZED)

# Profile, update_profile, and change_password remain the same as Token version
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Get current user's profile information.
    """
    try:
        pessoa = request.user.pessoa
        serializer = PessoaSerializer(pessoa)
        return Response(serializer.data)
    except:
        return Response({
            'error': 'Pessoa profile not found for this user'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update current user's profile information.
    
    Allowed fields:
    - name
    - email
    - phone
    - address
    """
    try:
        pessoa = request.user.pessoa
        serializer = PessoaSerializer(pessoa, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'pessoa': serializer.data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({
            'error': 'Pessoa profile not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change user password.
    
    Required fields:
    - old_password: Current password
    - new_password: New password
    """
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response({
            'error': 'Please provide both old and new password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check old password
    if not user.check_password(old_password):
        return Response({
            'error': 'Old password is incorrect'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate new password
    try:
        validate_password(new_password, user)
    except ValidationError as e:
        return Response({
            'new_password': list(e.messages)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Set new password
    # Only difference from Token version is that we return new tokens after password change
    user.set_password(new_password)
    user.save()
    
    refresh = RefreshToken.for_user(user)

    return Response({
    'message': 'Password changed successfully',
    'refresh': str(refresh),
    'access': str(refresh.access_token),
})