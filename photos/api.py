# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from photos.models import Photo
from photos.serializers import PhotoSerializer, PhotoListSerializer
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from photos.views import PhotosQueryset


class PhotoListAPI(PhotosQueryset, ListCreateAPIView):
    queryset = Photo.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return PhotoSerializer if self.request.method == 'POST' else PhotoListSerializer

#Al heredar de la clase ListCreate nos hace directamente el metodo GET y POST
    # def get(self, request):
    #     photos =Photo.objects.all()
    #     serializer = PhotoSerializer(photos, many=True)
    #     return Response(serializer.data)

    def get_queryset(self):
        return self.get_photo_queryset(self.request)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) # Grabamos la foto con el owner del usuario autenticado

class PhotoDetailAPI(PhotosQueryset, RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return self.get_photo_queryset(self.request)