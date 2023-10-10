from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    message = "You are not the superuser."
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False
    
class IsPostOwnerOrReadOnly(permissions.BasePermission):
    message = "You do not have permission to perform this action. You are not the owner of the post."
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user