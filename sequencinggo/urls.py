from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from posts.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('account.urls')),
    url(r'^posts/', include('posts.urls', namespace='posts')),
    # python-social-auth
    url('social-auth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^sitemap\.xml$',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^event/', include('event.urls', namespace='event')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
