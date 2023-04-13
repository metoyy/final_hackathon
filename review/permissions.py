from rest_framework import permissions

class IsUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.user == obj.user
