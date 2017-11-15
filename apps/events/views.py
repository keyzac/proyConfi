from django.shortcuts import render
from .serializers import *
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import pagination, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from pprint import pprint


class ListTagEventsAPIView(generics.ListAPIView):
    serializer_class = ListTagandEventSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = PageNumberPagination
    search_fields = ('name',)

    def get_queryset(self):
        return Tag.objects.all()


class ListTematicAPIView(generics.ListAPIView):
    serializer_class = ListTematicandEventSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Tematic.objects.all()


class ListPlaceAPIView(generics.ListAPIView):
    serializer_class = ListPlaceSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        return Place.objects.all()


class ListTagAPIView(generics.ListAPIView):
    serializer_class = ListTagSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        return Tag.objects.all()


class DetailEventAPIView(generics.ListAPIView):
    serializer_class = DetailEventSerializer

    def get_queryset(self):
        return Event.objects.filter(id=self.kwargs['pk'])


class DetailPonentAPIView(generics.ListAPIView):
    serializer_class = DetailPonentsSerializer

    def get_queryset(self):
        return Ponent.objects.filter(id=self.kwargs['pk'])

# Create your views here.
