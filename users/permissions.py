# sistema de permisos segun rol de ususario

from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role and request.user.role.name.lower() == 'admin')
    
class IsClient(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role and request.user.role.name.lower() == 'client')