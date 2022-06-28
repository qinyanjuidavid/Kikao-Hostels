from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsStudent(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "Student":
            return True
        if request.method in SAFE_METHODS:
            return True
        return False


class IsAdministrator(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "Administrator":
            return True
        if request.method in SAFE_METHODS:
            return True
        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == "Administrator":
            return True
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == "Administrator"
