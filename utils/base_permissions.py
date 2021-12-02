from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


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


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_admin or request.method in SAFE_METHODS:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_admin or request.method in SAFE_METHODS:
            return True
        else:
            return False
