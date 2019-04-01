from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            if request.user.user_type == 'Client':
                return True
            else:
                return str(obj.dealer) == str(request.user)

        # Write permissions are only allowed to the owner of the snippet.
        #print(str(obj.dealer) == str(request.user))
        # print(obj.dealer)
        # print(request.user)
        return str(obj.dealer) == str(request.user)

from rest_framework.permissions import IsAdminUser, SAFE_METHODS

class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super(
            IsAdminUserOrReadOnly, 
            self).has_permission(request, view)
        # Python3: is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin

class IsDealer(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            if request.user.user_type == 'Client':
                return False
            else:
                return str(obj.dealer) == str(request.user)

        # Write permissions are only allowed to the owner of the snippet.
        #print(str(obj.dealer) == str(request.user))
        # print(obj.dealer)
        # print(request.user)
        return str(obj.dealer) == str(request.user)
        
    class IsClient(permissions.BasePermission):
        """
        Custom permission to only allow owners of an object to edit it.
        """

        def has_object_permission(self, request, view, obj):
            # Read permissions are allowed to any request,
            # so we'll always allow GET, HEAD or OPTIONS requests.
            if request.method in permissions.SAFE_METHODS:
                if request.user.user_type == 'Client':
                    return True
                else:
                    return False

            # Write permissions are only allowed to the owner of the snippet.
            #print(str(obj.dealer) == str(request.user))
            # print(obj.dealer)
            # print(request.user)
            return False
