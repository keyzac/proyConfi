from rest_framework import serializers
from .models import *
from datetime import timedelta


class PlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'name')


class PonentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ponent
        fields = ('id', 'full_name', 'image', 'description')


class TematicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tematic
        fields = ('id', 'name', 'description', 'image')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class EventSerializer(serializers.ModelSerializer):
    ponents = PonentsSerializer(many=True, read_only=True)
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    not_server_hour = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'not_server_hour', 'title', 'content', 'date', 'image', 'ponents')


class ListTagandEventSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'frequency', 'events')


class ListTematicandEventSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Tematic
        fields = ('id', 'name', 'description', 'image', 'events')


class ListPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'longitude', 'latitude', 'name', 'image')


class ListTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'frequency')


class DetailEventSerializer(serializers.ModelSerializer):
    ponents = PonentsSerializer(many=True, read_only=True)
    places = PlacesSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'date', 'content', 'image', 'type', 'ponents', 'places')


class DetailPonentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ponent
        fields = ('id', 'full_name', 'description', 'image', 'twitter', 'facebook', 'google', 'linkdn')
