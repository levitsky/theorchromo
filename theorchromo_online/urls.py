from django.urls import path, re_path
from django.views.static import serve
from .views import *
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Example:
    # (r'^theorchromo_online/', include('theorchromo_online.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # path("admin/", admin.site.urls),
    re_path(r'^$', index),
    re_path(r'^help/$', help_page),
    re_path(r'^results/$', results),
]

if settings.DEBUG:
    urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
   ]
