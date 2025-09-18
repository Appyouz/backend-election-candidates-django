from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class IsSuper(permissions.BasePermission):
    """
    Allows access only to super.
    """

    message = "You are not authenticated to perform this action"

    def has_permission(self, request, view):
        return request.user.role == User.Roles.SUPER

    def has_object_permission(self, request, view, obj):
        return request.user.role == User.Roles.SUPER


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admin.
    """

    message = "You are not authenticated to perform this action"

    def has_permission(self, request, view):
        return request.user.role == User.Roles.ADMIN

    def has_object_permission(self, request, view, obj):
        return request.user.role == User.Roles.ADMIN


class IsMember(permissions.BasePermission):
    """
    Allows access only to member.
    """

    message = "You are not authenticated to perform this action"

    def has_permission(self, request, view):
        return request.user.role == User.Roles.MEMBER

    def has_object_permission(self, request, view, obj):
        return request.user.role == User.Roles.MEMBER
