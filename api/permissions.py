from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_owner = obj.user == request.user
        if request.method in SAFE_METHODS:
            return request.user.groups.filter(name='модератор').exists() or is_owner

        return is_owner


# class IsModerator(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name='модератор').exists()
