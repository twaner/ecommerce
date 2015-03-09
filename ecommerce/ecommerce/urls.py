from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = patterns('',
    # product views
    url(r'^$', 'products.views.home', name='home'),
    url(r'^products/$', 'products.views.allview', name='products'),
    url(r'^products/(?P<slug>[\w-]+)/$', 'products.views.single', name='single_product'), # Only accepts a slug, no whitespace.
    #(?P<all_items>.*)/$ or (?P<id>\d+)/$
    # admin
    url(r'^admin/', include(admin.site.urls)),
)

# Only use for serving during development. Files will not be served from django files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)