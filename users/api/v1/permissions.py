
from rest_framework import permissions

class CustomerAccessPermission(permissions.BasePermission):
    message = 'Adding permission , such that user can access only its info.'

    def has_object_permission(self, request, view, obj):
        if (request.user.mobile == obj.mobile) or request.user.is_superuser:
            return True
