# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.generic import View
from users.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from users.permissions import UserPermission


class UserListAPI(APIView):

    permission_classes = (UserPermission,)

    def get (self,request):
        self.check_permissions(request)
        paginator = PageNumberPagination() # Instaciamos el paginador
        users = User.objects.all()
        paginator.paginate_queryset(users,request) # Paginar el queryset
        serializer = UserSerializer(users,many=True)
        serializer_users = serializer.data #lista de diccionarios
        ####################################################
        #Como ahora heredamos de APIView esta parte nos lo podemos ahorrar, porque ya se encarga de renderizar
        # JSON/diccionario
        # renderer = JSONRenderer()
        # json_users = renderer.render(serializer_users) #lista de diccionarios -> JSON
        # return HttpResponse(json_users)
        ######################################################
        return paginator.get_paginated_response(serializer_users)

    def post(self, request):
        self.check_permissions(request)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED) #devolvemos lo grado como acuse de recibo
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPI(APIView):

    permission_classes = (UserPermission,)

    def get(self, request, pk):
        self.check_permissions(request)
        user = get_object_or_404(User,pk=pk) #usuario existe o no en la base de datos
        serializer = UserSerializer(user) # es un diccionario
        return Response(serializer.data) # el framework se encarga de convertir a JSON/XML

    def put(self, request, pk):
        self.check_permissions(request)
        user = get_object_or_404(User, pk=pk) #usuario existe o no en la base de datos
        self.check_object_permissions(request, user)
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.check_permissions(request)
        user = get_object_or_404(User, pk=pk)  # usuario existe o no en la base de datos
        self.check_object_permissions(request, user)
        user.delete()
        return  Response(status=status.HTTP_204_NO_CONTENT)
