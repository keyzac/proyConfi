from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^listtagandevents/$', ListTagEventsAPIView.as_view()),
    url(r'^listtematicandevents/$', ListTematicAPIView.as_view()),
    url(r'^listplace/$', ListPlaceAPIView.as_view()),
    url(r'^listtag/$', ListTagAPIView.as_view()),
    url(r'^detailevents/(?P<pk>\d+)/$', DetailEventAPIView.as_view()),
    url(r'^detailponents/(?P<pk>\d+)/$', DetailPonentAPIView.as_view()),

]
