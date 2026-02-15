from rest_framework import permissions


class IsPessoaOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow pessoas of an object to edit it.
    Assumes the model instance has an `pessoa` attribute.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the pessoa
        # Handle different object types
        if hasattr(obj, 'pessoa'):
            # For Pet model
            return obj.pessoa.user == request.user
        elif hasattr(obj, 'user'):
            # For pessoa model
            return obj.user == request.user
        elif hasattr(obj, 'pet'):
            # For VaccinationRecord model
            return obj.pet.pessoa.user == request.user
        
        return False


class IsPessoa(permissions.BasePermission):
    """
    Permission to only allow pessoas to access their own data.
    """
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'pessoa'):
            return obj.pessoa.user == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'pet'):
            return obj.pet.pessoa.user == request.user
        
        return False