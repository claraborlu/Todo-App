# permissions.py
from rest_framework import permissions

class IsOwnerOrSuperuser(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or superusers to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the task or a superuser.
        return obj.user == request.user or request.user.is_superuser
