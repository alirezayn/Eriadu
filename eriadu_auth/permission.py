# myapp/permissions.py

from rest_framework import permissions

class IsStaffUser(permissions.BasePermission):
    """
    Custom permission to only allow access to staff users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

# class IsMoshaver(permissions.BasePermission):
#      def has_permission(self, request, view):
#         return request.user.is_authenticated and getattr(request.user, 'is_moshaver', False)
