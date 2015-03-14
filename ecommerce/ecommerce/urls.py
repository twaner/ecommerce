from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Product views
    url(r'^$', 'products.views.home', name='home'),
    url(r'^s/$', 'products.views.search', name='search'),
    url(r'^products/$', 'products.views.allview', name='products'),
    url(r'^products/(?P<slug>[\w-]+)/$', 'products.views.single', name='single_product'), # Only accepts a slug, no whitespace.
    #(?P<all_items>.*)/$ or (?P<id>\d+)/$

    # Cart Views
    url(r'^cart/$', 'carts.views.view', name='cart'),
    url(r'^cart/(?P<id>\d+)/$', 'carts.views.remove_from_cart', name='remove_from_cart'),
    url(r'^cart/(?P<slug>[\w-]+)/$', 'carts.views.add_to_cart', name='add_to_cart'),

    # Products
    url(r'^checkout/$', 'orders.views.checkout', name='checkout'),
    url(r'^orders/$', 'orders.views.orders', name='orders'),

    # Accounts
    url(r'^accounts/logout/$', 'accounts.views.logout_view', name='auth_logout'),

    # admin
    url(r'^admin/', include(admin.site.urls)),
)

# Only use for serving during development. Files will not be served from django files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)