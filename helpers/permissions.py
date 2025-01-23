from rest_framework import permissions

class IsModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        
        if request.method == 'GET':
            return True
            
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        
        if request.method == 'GET':
            return True
            
        if request.user.role == 'moderator' and \
            request.user.status == 'verified':
            return True
        return False
    
class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'moderator' and \
            request.user.status == 'verified':
            return True
        return False


class IsModeratorOrIsTeacherOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        
        if request.method == 'GET':
            return True
            
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        
        if request.method == 'GET':
            return True
            
        if request.user.role == 'moderator' and \
            request.user.status == 'verified':
            return True
        return False


class IsModeratorOrIsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        
        if request.user.is_authenticated and \
            request.user.role:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        
        if request.user.role == 'moderator' and \
            request.user.status == 'verified':
            return True
        return False
    

class IsTeacherOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'teacher' and \
            request.user.status == 'verified':
            return True
        return False
        
class IsStudentOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'student' and \
            request.user.status == 'verified':
            return True
        return False

class IsMyAccountOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return False

class IsMyOrganizationOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        if request.user.is_authenticated:
            return True
    
    def has_object_permission(self, request, view, obj):
        
        if request.method == 'GET':
            return True
            
        if obj.moderator == request.user:
            return True
        
        return 