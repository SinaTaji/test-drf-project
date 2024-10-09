from rest_framework.permissions import BasePermission


class IsAuthenticatedRedirect(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated
