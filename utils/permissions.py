from django.shortcuts import get_object_or_404
from rest_framework import permissions

from apartments.models import Apartment


class IsAgent(permissions.BasePermission):
    message = "Only users that are agent can access this endpoint"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_agent)


class IsOwner(permissions.BasePermission):
    # This Permission checks for changes to the Apartment

    message = "Only apartment owners/agents can make changes to their apartments"

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )  # Equivalent to IsAuthenticated or ReadOnly

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            return obj.agent == request.user
        except Exception:
            # In a case when a user object is the instance to be checked
            return obj == request.user


class IsFileOwner(permissions.BasePermission):
    """
    This permission checks for changes to pictures and media of an apartment
    """

    message = "cannot make changes to other's apartment pictures/videos"

    def has_permission(self, request, view):
        apartment = get_object_or_404(Apartment, pk=int(view.kwargs["apartment_pk"]))

        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and (apartment.agent == request.user)
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.apartment.agent == request.user
