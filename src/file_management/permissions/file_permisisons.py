from rest_framework.permissions import BasePermission


class CanRetrieveFilePermission(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:  # type: ignore
        user = request.user
        if not user.is_authenticated or not user.is_active:
            return False

        if user.is_superuser:
            return True

        return user.has_perm("file_management.can_view_file")  # type: ignore[no-any-return]


class CanListFilePermission(BasePermission):
    def has_permission(self, request, view) -> bool:  # type: ignore
        user = request.user
        if not user.is_authenticated or not user.is_active:
            return False

        if user.is_superuser:
            return True

        return user.has_perm("file_management.can_view_file")  # type: ignore[no-any-return]


class CanUploadFilePermission(BasePermission):
    def has_permission(self, request, view) -> bool:  # type: ignore
        user = request.user
        if not user.is_authenticated or not user.is_active:
            return False

        if user.is_superuser:
            return True

        return user.has_perm("file_management.can_create_file")  # type: ignore[no-any-return]


class CanDeleteFilePermission(BasePermission):
    def has_permission(self, request, view) -> bool:  # type: ignore
        user = request.user
        if not user.is_authenticated or not user.is_active:
            return False

        if user.is_superuser:
            return True

        return user.has_perm("file_management.can_delete_file")  # type: ignore[no-any-return]
