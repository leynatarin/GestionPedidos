from django.conf.urls import patterns, include, url
from django.conf import settings
from registro.views import *
from GestionPedidos.views import *
from django.contrib import admin
from django.contrib.auth.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'GestionPedidos.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^menu/$', menu, name='menu'),
    url(r'^servicios/$', servicios, name='servicios'),
	url(r'^entradas/$', entradas, name='entradas'),
	url(r'^menuInfantil/$', menuInfantil, name='menuInfantil'),
	url(r'^perrosCalientes/$', perrosCalientes, name='perrosCalientes'),
	url(r'^hamburguesas/$', hamburguesas, name='hamburguesas'),
    url(r'^parrilla/$', parrilla, name='parrilla'),
    url(r'^pescados/$', pescados, name='pescados'),
    url(r'^sandwich/$', sandwich, name='sandwich'),
    url(r'^salchipapas/$', salchipapas, name='salchipapas'),
    url(r'^tostadas/$', tostadas, name='tostadas'),
    url(r'^ensaladas/$', ensaladas, name='ensaladas'),
    url(r'^desgranados/$', desgranados, name='desgranados'),
    url(r'^bebidas/$', bebidas, name='bebidas'),
    url(r'^agregarProducto/(\d+)$', agregarProducto, name='agregarProducto'),
    url(r'^carritoCompra/$', carritoCompra, name='carritoCompra'),
    url(r'^ordenCompra/$', ordenCompra, name='ordenCompra'),
    url(r'^confirmacionPedido/$', confirmacionPedido, name='confirmacionPedido'),
    url(r'^listaPedidos/$', listaPedidos, name='listaPedidos'),
    url(r'^detallePedido/(\d+)$', detallePedido, name='detallePedido'),
 
	url(r'^inicio/$', inicio, name='inicio'),
    url(r'^registro/$', registro, name='registro'),
    url(r'^editarPerfil/$', editarPerfil, name='editarPerfil'),
    url(r'^login/$', login, {'template_name': 'login.html', }, name="login"),
    url(r'^logout/$', logout, {'template_name': 'inicio.html', }, name="logout"),
    url(r'^admin/', include(admin.site.urls)),

    # Activamos la url de los mediafiles
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
)
