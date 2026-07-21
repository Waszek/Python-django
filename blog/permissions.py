from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE.METHODS = GET, OPTIONS, HEAD
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return  obj.user.name == request.user.username