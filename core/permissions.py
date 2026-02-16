from rest_framework import permissions


class IsPessoaOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read permissions are allowed to authenticated users.
    """
    
    message = "You do not have permission to modify this resource."
    
    def has_permission(self, request, view):
        """Check if user is authenticated"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Read permissions for any authenticated user.
        Write permissions only for the owner.
        """
        # Read permissions (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Staff users have full access
        if request.user.is_staff:
            return True
        
        # Check ownership based on object type
        return self._check_ownership(request.user, obj)
    
    def _check_ownership(self, user, obj):
        """
        Determine ownership based on object type.
        FIXED: Returns False instead of raising PermissionDenied
        """
        # Pet model
        if hasattr(obj, 'pessoa') and hasattr(obj.pessoa, 'user'):
            return obj.pessoa.user == user
        
        # Pessoa model
        if hasattr(obj, 'user'):
            return obj.user == user
        
        # VaccinationRecord model
        if hasattr(obj, 'pet') and hasattr(obj.pet, 'pessoa'):
            return obj.pet.pessoa.user == user
        
        # Default: deny access
        return False


class IsPessoa(permissions.BasePermission):
    """
    Strict permission - only owners can access.
    No read access for non-owners.
    """
    
    message = "You can only access your own resources."
    
    def has_permission(self, request, view):
        """Check if user is authenticated"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Only owners can access"""
        # Staff users have full access
        if request.user.is_staff:
            return True
        
        # Check ownership - FIXED: Returns False instead of raising
        return self._check_ownership(request.user, obj)
    
    def _check_ownership(self, user, obj):
        """
        Determine ownership.
        FIXED: Returns False instead of raising PermissionDenied
        """
        if hasattr(obj, 'pessoa') and hasattr(obj.pessoa, 'user'):
            return obj.pessoa.user == user
        
        if hasattr(obj, 'user'):
            return obj.user == user
        
        if hasattr(obj, 'pet') and hasattr(obj.pet, 'pessoa'):
            return obj.pet.pessoa.user == user
        
        return False


class IsPessoaOrAdmin(permissions.BasePermission):
    """
    Permission for sensitive operations.
    Only owner or admin staff can access.
    """
    
    message = "You can only access your own resources or must be an admin."
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin staff can access everything
        if request.user.is_staff:
            return True
        
        # Owner can access their own resources
        if hasattr(obj, 'pessoa') and hasattr(obj.pessoa, 'user'):
            return obj.pessoa.user == request.user
        
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        if hasattr(obj, 'pet') and hasattr(obj.pet, 'pessoa'):
            return obj.pet.pessoa.user == request.user
        
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission for resources that should be managed by admins only.
    Regular users can only read.
    """
    
    message = "Only administrators can modify this resource."
    
    def has_permission(self, request, view):
        # Everyone can read
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Only staff can write
        return request.user and request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        # Everyone can read
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only staff can write
        return request.user.is_staff