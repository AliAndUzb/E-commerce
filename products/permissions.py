from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    """ Custom permission to only allow owners to edit and delete their orders"""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so, we will always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return obj.owner == request.user


class IsStaffOrReadOnly(permissions.BasePermission):

    """ Custom permissions to only allow staff members to edit and delete products """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff
