from rest_framework import permissions
from users.permissions import IsModerator, IsObjectOwner, IsNotModerator


class CoursePermissions(permissions.BasePermission):
    """
    Права доступа для курсов:
    - Создавать: может любой авторизованный пользователь, кроме модератора
    - Просматривать: все авторизованные пользователи
    - Обновлять: владелец курса ИЛИ модератор
    - Удалять: только владелец курса И НЕ модератор
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action == 'create':
            return IsNotModerator().has_permission(request, view)

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action in ['update', 'partial_update']:
            return (IsObjectOwner().has_object_permission(request, view, obj) or
                    IsModerator().has_permission(request, view))

        if view.action == 'destroy':
            return (IsObjectOwner().has_object_permission(request, view, obj) and
                    IsNotModerator().has_permission(request, view))

        return False


class LessonPermissions(CoursePermissions):
    """
    Права доступа для уроков (аналогично курсам)
    """
    pass