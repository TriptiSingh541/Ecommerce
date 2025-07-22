from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Allow full access to admin users. Read-only access to others.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            (request.user and request.user.is_authenticated and request.user.is_staff)
        )