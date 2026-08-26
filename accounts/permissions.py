from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    Разрешает изменение (POST/PUT/PATCH/DELETE) только пользователям с ролью 'admin'.
    Чтение (GET) доступно всем аутентифицированным пользователям.
    """
    message = "Изменение справочников доступно только администратору."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return bool(request.user and request.user.is_authenticated and request.user.role == "admin")