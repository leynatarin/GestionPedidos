from django.conf.urls import patterns, url
from django.conf import settings
from .views import *

urlpatterns = patterns('',
    url(r'^$', inicio, name='inicio'),
    url(r'^inicio/$', inicio, name='inicio'),
    url(r'^menu/$', menu, name='menu'),
    url(r'^servicios/$', servicios, name='servicios'),
    url(r'^verCategoria/(\d+)$', verCategoria, name='verCategoria'),
    url(r'^agregarProducto/(\d+)$', agregarProducto, name='agregarProducto'),
    url(r'^eliminarProducto/(\d+)$', eliminarProducto, name='eliminarProducto'),
    url(r'^carritoCompra/$', carritoCompra, name='carritoCompra'),
    url(r'^ordenCompra/$', ordenCompra, name='ordenCompra'),
    url(r'^confirmacionPedido/$', confirmacionPedido, name='confirmacionPedido'),
    url(r'^listaPedidos/$', listaPedidos, name='listaPedidos'),
    url(r'^detallePedido/(\d+)$', detallePedido, name='detallePedido'),
    url(r'^historialCompra/$', historialCompra, name='historialCompra'),
)
