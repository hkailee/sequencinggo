from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.conference_list, name='conference_list'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.conference_list, name='conference_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.conference_detail, name='conference_detail'),
]
