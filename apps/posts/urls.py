from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^posts/$', ListRandomPostAPIView.as_view()),
    url(r'^users/(?P<pk>\d+)/posts/$', ListPostAPIView.as_view()),
    url(r'^users/posts/create/$', CreatePostAPIView.as_view()),
    url(r'^users/posts/(?P<pk>\d+)/comment/$', CreateCommentAPIView.as_view()),
    url(r'^users/posts/(?P<pk>\d+)/like/$', LikeCommentAPIView.as_view()),
    url(r'^users/posts/(?P<pk>\d+)/dislike/$', DisLikeCommentAPIView.as_view()),
    url(r'^users/posts/(?P<pk>\d+)/delete/$', DeletePostAPIView.as_view()),
    url(r'^users/posts/comment/(?P<pk>\d+)/delete/$', DeleteCommentAPIView.as_view()),
]
