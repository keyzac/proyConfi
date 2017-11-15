from django.shortcuts import render
from .serializers import *
from ..account.models import *
from ..events.models import *
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import pagination, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class CreatePostAPIView(generics.CreateAPIView):
    serializer_class = CreatePostSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        postserializer = ListPostSerializer(post, context={'request': request})

        return Response(postserializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class LikeCommentAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        for like in post.likes:
            if like.get('id') == self.request.user.id:
                return Response({'detail': 'not like'}, status=status.HTTP_303_SEE_OTHER)

        like = {'id': self.request.user.id, 'name': self.request.user.get_full_name()}
        post.likes.append(like)
        post.save()
        return Response({'detail': 'LIKE OK'}, status=status.HTTP_200_OK)


class DisLikeCommentAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        for like in post.likes:
            if like.get('id') == self.request.user.id:
                post.likes.remove(like)
                post.save()
        return Response({'detail': 'DISLIKE OK'}, status=status.HTTP_200_OK)


class ListPostAPIView(generics.ListAPIView):
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = ListPostSerializer

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs.get('pk'))
        return user.posts.filter(is_enable=True).prefetch_related('comments')


class CreateCommentAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateCommentsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = self.perform_create(serializer)
        commentserializer = CommentSerializer(comment, context={'request': request})
        headers = self.get_success_headers(serializer.data)
        return Response(commentserializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        comment = serializer.save(user=self.request.user, post=post)
        return comment


class DeletePostAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        delete = get_object_or_404(Post, id=self.kwargs.get('pk'))
        print(delete.user)
        print(self.request.user)
        if delete.user == self.request.user:
            delete.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No puedes borrar un post que no es tuyo'}, status=status.HTTP_200_OK)


class DeleteCommentAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        delete = get_object_or_404(Comment, id=self.kwargs.get('pk'))
        if delete.user == self.request.user:
            delete.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No puedes borrar un comentario que no es tuyo'}, status=status.HTTP_200_OK)

    def get_object(self):
        return get_object_or_404(self.request.user.comments, id=self.kwargs.get('pk'))


class ListRandomPostAPIView(generics.ListAPIView):
    serializer_class = ListPostSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Post.objects.filter(is_enable=True).prefetch_related('comments')

# Create your views here.
