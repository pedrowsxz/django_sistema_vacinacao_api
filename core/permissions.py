from rest_framework import permissions


class IsPessoaOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada para permitir que apenas os donos de um objeto possam editá-lo.
    Permissões de leitura são permitidas para usuários autenticados.
    """
    
    message = "Você não tem permissão para modificar este recurso."
    
    def has_permission(self, request, view):
        """Verifica se o usuário está autenticado"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Permissões de leitura para qualquer usuário autenticado.
        Permissões de edição apenas para o proprietário.
        """
        # Read permissions (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Usuários staff têm acesso total
        if request.user.is_staff:
            return True
        
        # Verifica a relação pessoa-pet com base no tipo de objeto
        return self._check_ownership(request.user, obj)
    
    def _check_ownership(self, user, obj):
        """
        Determina a relação pessoa-pet com base no tipo de objeto.
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
        
        # Padrão: rejeitar accesso
        return False


class IsPessoa(permissions.BasePermission):
    """
    Permissão estrita - apenas os proprietários podem acessar.
    Sem acesso de leitura para não proprietários.
    """
    
    message = "Você só pode acessar seus próprios recursos."
    
    def has_permission(self, request, view):
        """Verifica se o usuário está autenticado"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Apenas os proprietários podem acessar"""
        # Usuários staff têm acesso total
        if request.user.is_staff:
            return True
        
        # Verifica relação pessoa-pet
        return self._check_ownership(request.user, obj)
    
    def _check_ownership(self, user, obj):
        """
        Determina a relação entre pessoa e pet.
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
    Permissão para operações sensíveis.
    Apenas o proprietário ou usuários staff podem acessar.
    """
    
    message = "Você só pode acessar seus próprios recursos ou deve ser um administrador."
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Usuários staff/admin podem acessar tudo
        if request.user.is_staff:
            return True
        
        # A pessoa pode acessar seus próprios recursos
        if hasattr(obj, 'pessoa') and hasattr(obj.pessoa, 'user'):
            return obj.pessoa.user == request.user
        
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        if hasattr(obj, 'pet') and hasattr(obj.pet, 'pessoa'):
            return obj.pet.pessoa.user == request.user
        
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permissão para recursos que devem ser gerenciados apenas por administradores.
    Usuários comuns podem apenas ler.
    """
    
    message = "Apenas administradores podem modificar este recurso."
    
    def has_permission(self, request, view):
        # Todos podem ler
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Apenas staff/admin podem escrever
        return request.user and request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        # Todos podem ler
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Apenas staff/admin podem escrever
        return request.user.is_staff