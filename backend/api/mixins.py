from .permissions import IsStaffEditorPermission
from rest_framework.permissions import IsAdminUser


class StaffEditorPermissionMixin():
    """Mixin class for Staff Editor Permissions."""
    permission_classes = [IsAdminUser, IsStaffEditorPermission]


class UserQuerySetMixin():
    """Query Set mixin for filtering user data."""
    user_field = 'user'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = self.request.user
        qs = super().get_queryset(*args, **kwargs)
        if user.is_staff:
            return qs
        return qs.filter(**lookup_data)
