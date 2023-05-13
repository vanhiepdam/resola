from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class NoPermission(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return False
