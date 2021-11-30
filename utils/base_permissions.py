from rest_framework import permissions


class AdminRequired(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return user.is_admin

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if obj.pk == user.pk:
                return True
            return user.is_admin