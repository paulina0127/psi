from rest_framework import permissions


class IsCurrentUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.user == obj.owner:
            return True
        else:
            return False

    def has_view_permission(self, request, obj):
        if request.user.is_superuser:
            return True
        elif request.user == obj.owner:
            return True
        else:
            return False

    def has_change_permission(self, request, obj):
        if request.user.is_superuser:
            return True
        elif request.user == obj.owner:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj):
        if request.user.is_superuser:
            return True
        elif request.user == obj.owner:
            return True
        else:
            return False


class IsCurrentUserAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.user.username == obj.username:
            return True
        else:
            return False

    def has_view_permission(self, request, obj):
        if request.user.is_superuser:
            return True
        elif request.user.username == obj.username:
            return True
        else:
            return False

    def has_change_permission(self, request, obj):
        if request.user.is_superuser:
            return True
        elif request.user.username == obj.username:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj):
        if request.user.is_superuser:
            return True
        elif request.user.username == obj.username:
            return True
        else:
            return False
