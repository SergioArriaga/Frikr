# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseNotFound

from django.shortcuts import render
from photos.models import Photo
from photos.forms import PhotoForm
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView
from django.db.models import Q


class PhotosQueryset(object):

    def get_photo_queryset(self, request):
        if not request.user.is_authenticated():  # si no esta autenticado
            photos = Photo.objects.filter(visibility='PUBLIC')
        elif request.user.is_superuser:  # si es administrador
            photos = Photo.objects.all()
        else:
            photos = Photo.objects.filter(Q(owner=request.user) | Q(visibility='PUBLIC'))
        return photos


class HomeView(View):

    def get(self, request):
        """
        Esta función devuelve el home de mi página
        :param request:
        :return:
        """
        photos = Photo.objects.all().order_by('-created_at')
        context = {
            'photos_list': photos[:5]
        }
        return render(request, 'photos/home.html', context)

class DetailView(View, PhotosQueryset):

    def get(self, request, pk):
        """
        Carga la página de detalle de una foto
        :param request: HttoRequest
        :param pk: id de la foto
        :return: HttpResponse
        """

        # También podriamos hacerlo de esta forma
        # try:
        #     photo = Photo.objects.get(pk=pk)
        # except Photo.DoesNotExist:
        #     photo = None
        # except Photo.MultipleObjects:
        #     photo = None
        #


        possible_photos = self.get_photo_queryset(request).filter(pk=pk).select_related('owner')

        photo = possible_photos[0] if len(possible_photos) >= 1 else None
        if photo is not None:
            # cargar la plantilla de detalle
            context = {
                'photo': photo
            }
            return render (request, 'photos/detail.html', context)
        return HttpResponseNotFound("No existe la foto") # 404 Not found


class CreateView(View):

    @method_decorator(login_required())
    def get(self, request):
        """
        Muestra un formulario para crear una foto
        :param request: HttoRequest
        :return: HttpResponse
        """
        form = PhotoForm()
        if form.is_valid():
            new_photo = form.save() # Guarda el objeto foto y me lo devuelve
            form = PhotoForm()
            success_message='Guardado con éxito!'
            success_message += ' <a href="{0}">'.format(reverse('photo_detail', args=[new_photo.pk]))
            success_message += 'Ver foto'
            success_message += '</a>'
        context = {
            'form': form,
            'success_message': ''
        }

        return render(request, 'photos/new_photo.html', context)

    @method_decorator(login_required())
    def post(self, request):
        """
        Muestra un formulario para crear una foto
        :param request: HttpRequest
        :return: HttpResponse
        """
        success_message = ''
        photo_with_owner = Photo()
        photo_with_owner.owner = request.user  # asigno como propietario de la foto al usuario autenticado
        form = PhotoForm(request.POST, instance=photo_with_owner)
        if form.is_valid():
            new_photo = form.save()  # Guarda el objeto foto y me lo devuelve
            form = PhotoForm()
            success_message = 'Guardado con éxito!'
            success_message += ' <a href="{0}">'.format(reverse('photo_detail', args=[new_photo.pk]))
            success_message += 'Ver foto'
            success_message += '</a>'
        context = {
            'form': form,
            'success_message': success_message
        }

        return render(request, 'photos/new_photo.html', context)

class PhotoListView(View, PhotosQueryset):

    def get(self, request):
        """
        Devuelve:
        - Las fotos públicas si el usuario no esta autenticado
        - Las fotos del usuario autenticado o las públicas de otros
        - Si el usuario es superadministrador, todas las fotos
        :param request: HttpRequest
        :return: HttpResponse
        """
        context = {
            'photos': self.get_photo_queryset(request)
        }
        return render(request, 'photos/photos_list.html', context)

class UserPhotosView(ListView):
    model = Photo
    template_name = 'photos/user_photos.html'

    def get_queryset(self):
        queryset = super(UserPhotosView, self).get_queryset()
        return queryset.filter(owner=self.request.user)

