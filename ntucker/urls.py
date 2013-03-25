from __future__ import unicode_literals
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from cms.sitemaps import CMSSitemap
from django.http import HttpResponse

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'cmspages': CMSSitemap}}),
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow:", mimetype="text/plain")),
    url(r'^', include('cms.urls')),
)
