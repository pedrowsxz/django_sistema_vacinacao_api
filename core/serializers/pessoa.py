from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Pessoa


class PessoaSerializer(serializers.ModelSerializer):
    """
    Serializer  para operações de listagem e criação de Pessoa.
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
    Serializer detalhado com informações dos pets.
    """
    pets = serializers.SerializerMethodField()
    
    class Meta(PessoaSerializer.Meta):
        fields = PessoaSerializer.Meta.fields + ['pets', 'updated_at']
    
    def get_pets(self, obj):
        """Retornar dados simplificados dos pets"""
        from core.serializers.pet import PetMinimalSerializer
        return PetMinimalSerializer(obj.pets.all(), many=True).data


class PessoaCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criar uma nova pessoa com conta de usuário.
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
        """Criar usuário e pessoa em uma única transação"""
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        
        # Criar usuário
        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=password
        )
        
        # Criar pessoa vinculada ao usuário
        pessoa = Pessoa.objects.create(user=user, **validated_data)
        return pessoa