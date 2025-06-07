from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only owners of an object to access it.
    Assumes the model instance has an `owner` attribute or user field.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsSender(permissions.BasePermission):
    """
    Allows only the sender of a message to access/modify it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user


class IsParticipant(permissions.BasePermission):
    """
    Allows only conversation participants to access the conversation.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()