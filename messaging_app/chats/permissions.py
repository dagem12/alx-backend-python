from rest_framework import permissions

class IsSender(permissions.BasePermission):
    """
    Allows only the sender of a message to access/modify it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user


class IsParticipant(permissions.BasePermission):
    """
    Allows only authenticated users who are participants of the conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
    
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False