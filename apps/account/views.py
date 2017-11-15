from django.shortcuts import render
from rest_framework import generics, status, filters
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from social.apps.django_app.utils import psa
from rest_framework.response import Response
from .serializers import *
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        token, created = Token.objects.get_or_create(user=serializer.get_user())
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class MobileLoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        token, created = Token.objects.get_or_create(user=serializer.get_user())
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class FacebookMobileLoginAPI(MobileLoginAPI):
    '''Facebook Login'''
    serializer_class = FacebookLoginSerializer

    @method_decorator(psa('account:facebook-mobile-login'))
    def dispatch(self, request, *args, **kwargs):
        return super(FacebookMobileLoginAPI, self).dispatch(request, *args, **kwargs)


class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class ChangePasswordAPIView(generics.GenericAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "OK"}, status=status.HTTP_200_OK)


class RecoveryPasswordAPI(generics.GenericAPIView):
    serializer_class = PasswordRecoverySerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "OK"}, status=status.HTTP_200_OK)


class RecoveryPasswordStep2API(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        credentials = self.retrieve_credentials()
        if credentials[0] and credentials[1]:
            return Response({"email": credentials[0].email}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        credentials = self.retrieve_credentials()
        if credentials[0] and credentials[1]:
            serializer = self.get_serializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=credentials[0])
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve_credentials(self):
        id = self.kwargs.get("id")
        user = User.objects.get(pk=id)
        token = default_token_generator.check_token(user, self.kwargs.get("token"))
        return user, token


class RetrieveUserAPIView(generics.RetrieveAPIView):
    serializer_class = RetrieveUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UpdateUserAPIView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class UpdateUserPhotoAPIView(generics.UpdateAPIView):
    '''Actualizer fotos del usuario'''
    permission_classes = IsAuthenticated,
    serializer_class = UpdateUserPhotoSerializer
    queryset = User.objects.all()


class FilterUsersAPIView(generics.ListAPIView):
    '''Filtrar usuarios por query params buscando por coincidencias en nombre o apellidos,ejemplo api/users/?search=erik'''
    queryset = User.objects.filter(is_superuser=False)
    pagination_class = PageNumberPagination
    serializer_class = UserFilterSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name')


class ListSongBook(generics.ListAPIView):
    queryset = Songbook.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = SongbookSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
