from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Pessoa


class PessoaSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Pessoa list and create operations.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    total_pets = serializers.ReadOnlyField()
    
    class Meta:
        model = Pessoa
        fields = [
            'id',
            'username',
            'name',
            'email',
            'phone',
            'address',
            'total_pets',
            'created_at'
        ]
        read_only_fields = ['created_at']


class PessoaDetailSerializer(PessoaSerializer):
    """
    Detailed serializer with nested pet information.
    """
    pets = serializers.SerializerMethodField()
    
    class Meta(PessoaSerializer.Meta):
        fields = PessoaSerializer.Meta.fields + ['pets', 'updated_at']
    
    def get_pets(self, obj):
        """Return simplified pet data"""
        from core.serializers.pet import PetMinimalSerializer
        return PetMinimalSerializer(obj.pets.all(), many=True).data


class PessoaCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new pessoa with user account.
    """
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = Pessoa
        fields = [
            'id',
            'username',
            'password',
            'name',
            'email',
            'phone',
            'address'
        ]
    
    def create(self, validated_data):
        """Create user and pessoa in one transaction"""
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=password
        )
        
        # Create pessoa linked to user
        pessoa = Pessoa.objects.create(user=user, **validated_data)
        return pessoa