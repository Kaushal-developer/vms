from rest_framework import permissions

from lib import constants


'''
Custome Permission handler for read /write
'''

class customReadWritePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request and request.user:
            return True
        else:
            return False

