from rest_framework.permissions import BasePermission

class IsOrganizer(BasePermission):
    message = "You are not the organizer of this article. Go away! You're naughty..."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or obj.organizer == request.user:
            return True
        return False