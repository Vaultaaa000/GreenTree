from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Allow only administrators to access
    """

    def has_permission(self, request, view):
        # allow superuser to access
        if request.user.is_superuser:
            return True
        return request.user and hasattr(request.user, 'role') and request.user.role == 'admin'


class IsHR(permissions.BasePermission):
    """
    Allow HR and administrators to access
    """

    def has_permission(self, request, view):
        # Allow superuser to access
        if request.user.is_superuser:
            return True
        return request.user and hasattr(request.user, 'role') and request.user.role in ['hr', 'admin']


class IsEmployee(permissions.BasePermission):
    """
    allow all user to access
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user and hasattr(request.user, 'role') and request.user.role in ['employee', 'hr', 'admin']


class IsOwnerOrHRAdmin(permissions.BasePermission):
    """
    Object-level permissions:
        - Admins and HR can access all employees’ data
        - Employees can only access their own data
    """

    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if not hasattr(request.user, 'role'):
            return False

        if request.user.role in ['admin', 'hr']:
            return True

        # Check whether it is your own data
        # For Employee
        if hasattr(obj, 'user_id') and obj.user_id is not None:
            return obj.user_id == request.user.id

        # For Attendance and Performance
        elif hasattr(obj, 'employee') and hasattr(obj.employee, 'user_id') and obj.employee.user_id is not None:
            return obj.employee.user_id == request.user.id

        elif hasattr(request.user, 'email'):
            if hasattr(obj, 'email'):
                return obj.email == request.user.email
            elif hasattr(obj, 'employee') and hasattr(obj.employee, 'email'):
                return obj.employee.email == request.user.email

        return False