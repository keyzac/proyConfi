from django.core.urlresolvers import reverse, reverse_lazy
from django.conf.urls import url
from .views import *
from django.contrib.auth import views

urlpatterns = [
    url(r'^register/$', CreateUserAPIView.as_view()),
    url(r'^user/retrieve/$', RetrieveUserAPIView.as_view()),
    url(r'^login/$', LoginAPIView.as_view()),
    url(r'^login/mobile/(?P<backend>[^/]+)/$', FacebookMobileLoginAPI.as_view(), name="facebook-mobile-login"),
    url(r'^password_reset/$', views.password_reset,
        {"post_reset_redirect": reverse_lazy('password_reset_done')},
        name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm,
        {"post_reset_redirect": reverse_lazy('password_reset_complete')},
        name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
    url(r'^user/recovery/$', RecoveryPasswordAPI.as_view()),
    url(r'^user/recovery/(?P<id>\d+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        RecoveryPasswordStep2API.as_view()),
    url(r'^filter/users/$', FilterUsersAPIView.as_view()),
    url(r'^user/update/$', UpdateUserAPIView.as_view()),
    url(r'^user/(?P<pk>\d+)/photo/$', UpdateUserPhotoAPIView.as_view()),
    url(r'^songbooks/$', ListSongBook.as_view()),

]
