from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from .views import *

urlpatterns = patterns('',
    url(r'^registro/$', registro, name='registro'),
    url(r'^editarPerfil/$', editarPerfil, name='editarPerfil'),
    url(r'^login/$', login, {'template_name': 'login.html', }, name="login"),
    url(r'^logout/$', logout, {'template_name': 'inicio.html', }, name="logout"),

    url(
        r'^cambioContrasena/$',
        password_reset,
        {'template_name': 'cambioContrasena.html', },
        name="password_reset"),
    url(
        r'^cambioContrasena/hecho/$',
        password_reset_done,
        {'template_name': 'cambioContrasenaHecho.html', },
        name="password_reset_done"),
    url(
        r'^cambioContrasena/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm, 
        {'post_reset_redirect' : '/cambioContrasena/completo/', 'template_name': 'cambioContrasenaConfirmacion.html',},
        name="password_reset_confirm"),
    url(
        r'^cambioContrasena/completo/$',
        password_reset_complete,
        {'template_name': 'cambioContrasenaCompleto.html', },
        name="password_reset_complete"),
)
