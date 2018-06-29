from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FormParser
from django.shortcuts import get_object_or_404


#To create directories
import os, shutil, errno
from django.conf import settings
import hashlib

from . import serializers
from . import models
from . import permissions

import logging
logger = logging.getLogger("__views__")

# Create your views here.

class HelloApiView(APIView):
    """Test API View."""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features."""

        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name."""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handles updating an object."""

        return Response({'method': 'put'})

    def patch(self, request, pk=None):
        """Patch request, only updates fields provided in the request."""

        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        """Deletes and object."""

        return Response({'method': 'delete'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet."""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message."""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code.'
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message."""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handles getting an object by its ID."""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handles updating an object."""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handles updating part of an object."""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handles removing an object."""

        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, creating and updating profiles."""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')

class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token."""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        if ObtainAuthToken().post(request).data:
            username = request.data.get("username")
            token = ObtainAuthToken().post(request).data['token']
            user_model = models.UserProfile.objects.get(email=username)
            plan_model = models.UserPlan.objects.get(user=user_model, status=1)
            try:
                user_history = models.UserProcessHistory.objects.get(user_profile = user_model, status = 1)
            except models.UserProcessHistory.DoesNotExist:
                user_history = models.UserProcessHistory(
                    user_profile = user_model,
                    description = "Login usuario",
                    full_storage = plan_model.plan.storage,
                    filled_storage = 0,
                    filled_storage_doc = 0,
                    filled_storage_music = 0,
                    filled_storage_video = 0,
                    filled_storage_image = 0
                )
                user_history.save()

            return Response({'token':token,
                            'name':user_model.name,
                            'lastname':user_model.lastname,
                            'plan_id':plan_model.plan.id,
                            'plan_name':plan_model.plan.name,
                            'plan_price':plan_model.plan.price,
                            'plan_storage':plan_model.plan.storage,
                            'plan_details':plan_model.plan.detail,
                            'filled_storage': user_history.filled_storage,
                            'filled_storage_doc': user_history.filled_storage_doc,
                            'filled_storage_music': user_history.filled_storage_music,
                            'filled_storage_video': user_history.filled_storage_video,
                            'filled_storage_image':user_history.filled_storage_image
                            })
        """Use the ObtainAuthToken APIView to validate and create a token."""
        return ObtainAuthToken().post(request)

class DeleteFileViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token."""
    serializer_class = serializers.DeleteFileSerializer

    def list(self,request):
        return Response({'Server Response': "URL para eliminar archivos"})

    def create(self, request):
        params = serializers.DeleteFileSerializer(data=request.data)
        if not params.is_valid():
            return Response({'Server Response': "URL a elimiminar no valida"})
        else:
            filename = params.data.get('filename')
            email = params.data.get('email')
            try:
                userfile_model = models.UserFile.objects.get(filename=filename,email=email)
            except models.UserFile.DoesNotExist:
                userfile_model = None
            if userfile_model != None:
                os.remove(os.path.join(settings.MEDIA_ROOT, userfile_model.url_docs + "/" + filename.replace(" ","_")))
                userfile_model.delete()
                return Response({'Server Response': filename})
            else:
                return Response({'Server Response': "No se encontraron candidatos"})

class UserProcessHistoryViewSet(viewsets.ModelViewSet):
    """Create the history of user status bar """

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.UserProcessHistorySerializer
    queryset = models.UserProcessHistory.objects.all()
    permission_classes = (permissions.SeeOwnStatus, IsAuthenticated)

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return models.UserProcessHistory.objects.filter(user_profile=user)


    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save()

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""

        serializer.save(user=self.request.user)

class ImageUploadViewSet(viewsets.ModelViewSet):
    """Cambie de lugares estas dos llamadas"""

    serializer_class = serializers.UploadImageSerializer
    queryset = models.Image.objects.all();

class FileUploadViewSet(viewsets.ModelViewSet):
    """Cambie de lugares estas dos llamadas"""

    serializer_class = serializers.UploadFileSerializer
    queryset = models.AnyFile.objects.all();

class PlanViewSet(viewsets.ModelViewSet):
    """Cambie de lugares estas dos llamadas"""

    serializer_class = serializers.PlanSerializer
    queryset = models.PlanType.objects.all();

class UserPlanViewSet(viewsets.ViewSet):

    serializer_class = serializers.UserPlanSerializer

    def list(self,request):
        params = serializers.GetUserPlanSerializer(data=request.query_params)
        if not params.is_valid():
            queryset = models.UserPlan.objects.all()
            serializer = serializers.ListUserPlanSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            email = request.query_params['email']
            user_model = models.UserProfile.objects.get(email=email, status=1)
            queryset = models.UserPlan.objects.filter(user = user_model)
            serializer = serializers.ListUserPlanSerializer(queryset, many=True)
            return Response(serializer.data)

    def create(self, request):
        """Create a new hello message."""

        serializer = serializers.UserPlanSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data.get('email')
            plan_id = serializer.data.get('plan_id')

            user_model = models.UserProfile.objects.get(email = email)
            plan_model = models.PlanType.objects.get(id = plan_id)

            userplan = models.UserPlan(
                user = user_model,
                plan = plan_model,
                status = 1
            )
            userplan.save()

            message = 'Email:{0} - Id Plan: {1}'.format(email,plan_id)
            return Response({'Server Response': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MultiUploadViewSet(viewsets.ModelViewSet):
    """Guarda una lista de archivos"""

    authentication_classes = (TokenAuthentication,)
    queryset = models.UserFile.objects.all()
    serializer_class = serializers.MultiUploadSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(MultiUploadViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            print("Ultimo")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        """This view should return a list of all files
        for the currently authenticated user."""
        user = self.request.user
        queryset = models.UserFile.objects.all()
        filetype = self.request.query_params.get('filetype', None)
        if filetype is not None:
            filetype_obj = models.Filetype.objects.filter(id=filetype)
            filtered_queryset = queryset.filter(filetype=filetype_obj, user=user)
            return filtered_queryset
        else:
            return queryset.filter(user=user)

class LoginCollectorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LoginCollectorSerializer

    def list(self,request):
        return Response({'Server Response': "Login de colectores"})

    def create(self, request):
        params = serializers.LoginCollectorSerializer(data=request.data)
        if params.is_valid():
            collector = get_object_or_404(models.UserCollector, collector_rut=params.data.get("rut"), password=params.data.get("password"))
            if collector is not None:
                serializer = serializers.CollectorSerializer(collector)
                return Response({'user': serializer.data})
            else:
                return Response({'Server Response': "Wrong credencials provided!"})
        else:
            return Response({'Server Response': "Problem with fields!"})

class AddCodeViewSet(viewsets.ModelViewSet):

    queryset = models.Codes.objects.all()
    serializer_class = serializers.AddCodeSerializer

    def list(self,request):
        return Response({'Server Response': "Add codes"})

    def create(self, request):
        params = serializers.AddCodeSerializer(data=request.data)
        if params.is_valid():
            collector = get_object_or_404(models.UserCollector, collector_rut=params.data.get("collector_rut"))
            if collector is not None:
                try:
                    code_model = models.Codes.objects.get(email=params.data.get("email"))
                    return Response({'code': "The email is already taken!"})
                except models.Codes.DoesNotExist:
                    try:
                        user = models.UserProfile.objects.get(email=params.data.get("email"))
                        return Response({'code': "The email already exist!"})
                    except models.UserProfile.DoesNotExist:
                        code = models.Codes(
                            collector = collector,
                            email = params.data.get("email"),
                            status = 1
                        )
                        code.save()
                        return Response({'code': params.data.get("email")})
            else:
                return Response({'Server Response': "Wrong credencials provided!"})
        else:
            return Response({'Server Response': "Problem with fields!"})

class ListCodesViewSet(viewsets.ModelViewSet):

    queryset = models.Codes.objects.all()
    serializer_class = serializers.ListCodesSerializer

    def list(self, request):
        return Response({'Server Response': "Obtener lista de referidos por colector"})

    def create(self, request):
        params = serializers.ListCodesSerializer(data=request.data)
        if params.is_valid():
            try:
                collector = models.UserCollector.objects.get(collector_rut=params.data.get("collector_rut"))
                try:
                    code_model = models.Codes.objects.filter(collector = collector)
                    serializer_response = serializers.ListCodesByUserSerializer(code_model, many=True)
                    return Response(serializer_response.data)
                except models.Codes.DoesNotExist:
                    return Response({'Server Response': "Ese usuario no tiene referidos aun"})
            except models.UserCollector.DoesNotExist:
                return Response({'Server Response': "Ese usuario no existe"})
        else:
            return Response({'Server Response': "Obtener lista de referidos por colector"})

class RegisterCollectorViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.RegisterCollectorSerializer

    def list(self, request):
        return Response({'Server Response': "Registrar a los colectores"})

    def create(self, request):
        params = serializers.RegisterCollectorSerializer(data=request.data)
        if params.is_valid():
            try:
                collector = models.UserCollector.objects.get(collector_rut=params.data.get("collector_rut"))
                return Response({'Server Response': "El usuario ya existe"})
            except models.UserCollector.DoesNotExist:
                collector_model = models.UserCollector(
                    collector_rut = params.data.get("collector_rut"),
                    name = params.data.get("name"),
                    password = params.data.get("password")
                )
                collector_model.save()
                return Response({'Server Response': "El usuario se ha agregado con exito"})
        else:
            return Response({'Server Response': "Problemas con los campos!"})
