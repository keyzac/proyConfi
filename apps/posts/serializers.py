from rest_framework import serializers
from ..account.models import User
from ..posts.models import *

__author__ = 'shinobu'


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'image', 'text']


class UserInCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'picture']


class CommentSerializer(serializers.ModelSerializer):
    user_firstname = serializers.CharField(source='user.first_name', read_only=True)
    user_lastname = serializers.CharField(source='user.last_name', read_only=True)
    user_photo = serializers.ImageField(source='user.picture', read_only=True)
    is_my_comment = serializers.SerializerMethodField()

    def get_is_my_comment(self, obj):
        band = False
        if self.context.get('request').user:
            user = self.context.get('request').user
            if user.is_authenticated():
                if obj.user == user:
                    band = True

        return band

    class Meta:
        model = Comment
        fields = ['id', 'text', 'user_firstname', 'user_lastname', 'user_photo', 'created_at', 'is_my_comment']


class UserInPostserializer(serializers.ModelSerializer):
    user = UserInCommentSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'picture', 'user']


class ListPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.JSONField(read_only=True)
    user = UserInPostserializer(read_only=True)
    is_like = serializers.SerializerMethodField()
    is_my_post = serializers.SerializerMethodField()
    num_likes = serializers.SerializerMethodField()

    def get_num_likes(self, obj):
        provisional_count = 0
        for like in obj.likes:
            provisional_count = provisional_count + 1
        return provisional_count

    def get_is_my_post(self, obj):
        band = False
        if self.context.get('request').user:
            user = self.context.get('request').user
            if user.is_authenticated():
                if obj.user == user:
                    band = True

        return band

    def get_is_like(self, obj):
        band = False
        if self.context.get('request').user.is_authenticated():
            user_id = self.context.get('request').user.id
            for like in obj.likes:
                if like.get('id') == user_id:
                    band = True
        return band

    class Meta:
        model = Post
        fields = ['id', 'created_at', 'text', 'image', 'num_likes', 'likes', 'is_like', 'comments',
                  'is_my_post',
                  'user']


class UserLikeSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    comment = serializers.CharField(required=True)


class CreateCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text']
