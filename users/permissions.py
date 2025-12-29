from rest_framework import permissions


class IsObjectOwner(permissions.BasePermission):
    """Является ли пользователь владельцем объекта"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user  # Сокращенная версия


class IsModerator(permissions.BasePermission):
    """Является ли пользователь модератором"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()