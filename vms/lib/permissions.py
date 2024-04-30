from rest_framework import permissions

from lib import constants


class customReadWritePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request and request.user:
            return True
        else:
            return False

