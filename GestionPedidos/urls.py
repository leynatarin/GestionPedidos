from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from restaurante import urlsRestaurante
from registro import urlsRegistro

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include(urlsRestaurante)),
    url(r'^', include(urlsRegistro)),
    url(r'^admin/', include(admin.site.urls)),
    # Activamos la url de los mediafiles
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
)
