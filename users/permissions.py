# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission

class UserPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Define si el usuario autenticado en request.user tiene permiso para realizar la acción (GET,POST,PUT o DELETE)
        :param request:
        :param view:
        :return:
        """
        from api import UserDetailAPI
        # si quiere crear un usuario, sea quien sea, puede
        if request.method == 'POST':
            return True
        # si bo es POST, el superusuario siempre puede
        elif request.user.is_superuser:
            return True
        # si es GET a la vista de detalle, tomo la decicisión en has_object_permissions
        elif isinstance(view, UserDetailAPI):
            return True
        else:
            # GET a /api/1.0/users/
            return False

    def has_object_permission(self, request, view, obj):
        """
        Define si el usuario autenticado en request.user tiene permiso para realizar la acción GET, PUT o DELETE)
        :param request:
        :param view:
        :param obj:
        :return:
        """
        return request.user.is_superuser or request.user == obj
