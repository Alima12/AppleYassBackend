from rest_framework import permissions


class AdminRequired(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_admin

    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.pk == user.pk:
            return True
        return user.is_admin


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return not user.is_authenticated
