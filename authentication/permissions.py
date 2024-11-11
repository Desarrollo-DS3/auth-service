
from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'

class IsWarehouseAssistant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'warehouse-assistant'
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == 'admin'
        #print(request.user.role)
        #return request.user.is_authenticated and request.user.role == 'admin'
