from django.conf.urls import url
from . import views
from .feeds import LatestPostsFeed

urlpatterns = [
    url(r'^create/$', views.post_create, name='create'),
    url(r'^detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.post_detail, name='detail'),
    url(r'^vote/$', views.post_vote, name='vote'),
    url(r'^mypost/$', views.mypost, name='mypost'),
    url(r'^remove/(?P<post_id>\d+)/$', views.post_remove, name='post_remove'),
    url(r'^edit/(?P<post_id>\d+)/$', views.post_edit, name='post_edit'),
    url(r'^ranking/$', views.post_mostviewed, name='ranking'),
    url(r'^$', views.post_list, name='list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', 'posts.views.post_list_by_tag', name="post_list_by_tag"),
    url(r'^(?P<post_id>\d+)/share/$', 'posts.views.post_share', name="post_share"),
    url(r'^feed/$', LatestPostsFeed(), name="post_feed"),
    url(r'^search/$', 'posts.views.post_search', name="post_search"),
]


