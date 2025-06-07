from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Allows only authenticated users who are participants of the conversation.
    Checks object-level permissions for all methods: GET, POST, PUT, PATCH, DELETE.
    """

    def has_permission(self, request, view):
   
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
    
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False


class IsSender(permissions.BasePermission):
    """
    Allows only the sender of a message to modify (PUT/PATCH/DELETE) their message.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.sender == request.user
        return True  