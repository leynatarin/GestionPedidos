# -*- coding: utf-8 -*-
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from recommends.tasks import recommends_precompute
from registro.models import *
import datetime

def inicio(request):
    return render_to_response('inicio.html', {'title': 'Inicio'}, context_instance=RequestContext(request))

def servicios(request):
    return render_to_response('servicios.html', {'title': 'Servicios'}, context_instance=RequestContext(request))

def menu(request):
    categorias = Categoria.objects.all();
    return render_to_response('menu.html', {'title': 'Menu', 'categorias_list': categorias}, context_instance=RequestContext(request))

def verCategoria(request, categoriaId):
    categoria = Categoria.objects.get(id=categoriaId);
    listaProductos = Producto.objects.filter(tipo=categoria);
    return render_to_response('detalleCategoria.html', {'title': categoria.nombre, 'listaProductos': listaProductos}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def agregarProducto(request, id_producto):
    product = Producto.objects.get(id=id_producto)
    if not 'carrito_compra' in request.session:
        request.session['carrito_compra'] = {}
    map_productos = request.session['carrito_compra']
    
    if map_productos.has_key(id_producto):
        map_productos[id_producto] = [map_productos[id_producto][0]+1]
    else:
        map_productos[id_producto] = [1]
    request.session['carrito_compra'] = map_productos

    return HttpResponseRedirect("/verCategoria/" + str(product.tipo.id))

def eliminarProducto(request, id_producto):
    if 'carrito_compra' in request.session:
        carrito = request.session['carrito_compra']
        del carrito[id_producto]
        if len(carrito) > 0:
            request.session['carrito_compra'] = carrito
        else:
            del request.session['carrito_compra']
    return HttpResponseRedirect("/carritoCompra/")

def carritoCompra(request):
    if 'carrito_compra' in request.session:
        carrito = request.session['carrito_compra']
        v_total = 0
        impuestos = 0
        for key, value in carrito.items():
            prod = Producto.objects.get(id=key)
            cantidad = value[0]
            subtotal = float(cantidad) * float(prod.precio)
            v_total += subtotal
            value.append(prod.nombre)
            value.append(prod.precio)
            value.append(subtotal)
        result = {'title': 'Carrito de Compra', 'total': int(v_total), "carrito": carrito}
        return render_to_response('carritoCompra.html', result, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/carritoCompraVacio/")

def ordenCompra(request):
    if 'carrito_compra' in request.session:
        carrito = request.session['carrito_compra']
        orden = OrdenCompra.objects.create(usuario=request.user, total=0, impuestos=0, fecha=datetime.datetime.now())
        v_total = 0;
        for key, value in carrito.items():
            prod = Producto.objects.get(id=key)
            cantidad = value[0]
            v_total += float(cantidad) * float(prod.precio)
            ordenProducto = OrdenProducto.objects.create(producto=prod, ordenCompra=orden, cantidad=cantidad)
            ordenProducto.save()
        orden.total = v_total
        orden.save()
        request.session['carrito_compra'] = {}
        recommends_precompute()
        return HttpResponseRedirect("/confirmacionPedido/")

def confirmacionPedido(request):
    return render_to_response('confirmacionPedido.html', context_instance=RequestContext(request))

def carritoCompraVacio(request):
    return render_to_response('carritoCompraVacio.html', context_instance=RequestContext(request))

def listaPedidos(request):
    ordenes = OrdenCompra.objects.all()
    return render_to_response('listaPedidos.html', {'ordenes': ordenes}, context_instance=RequestContext(request))

def detallePedido(request, id):
    orden = OrdenCompra.objects.get(id=id)
    perfil = Perfil.objects.get(user=orden.usuario)
    return render_to_response('detallePedido.html', {'ordenCompra': orden, 'perfil': perfil}, context_instance=RequestContext(request))

def historialCompra(request):
    ordenes = OrdenCompra.objects.filter(usuario=request.user)
    return render_to_response('historialCompra.html', {'ordenes': ordenes}, context_instance=RequestContext(request))

def enviarPedido(request, id_pedido):
    pedido = OrdenCompra.objects.get(id=id_pedido)
    usuario = pedido.usuario
    perfil = Perfil.objects.get(user=usuario)
    
    email_context = {
        'usuario': usuario,
        'perfil': perfil,
        'pedido': pedido
    }
    # se renderiza el template con el context
    email_html = render_to_string('email_confirmacion.html', email_context)
    # se quitan las etiquetas html para que quede en texto plano
    email_text = strip_tags(email_html)

    send_mail(
        'Confirmacion de Pedido',
        email_text,
        'maria.juana.tulua@gmail.com',
        [usuario.email,],
        html_message=email_html,
    )
 
    # se actualiza el estado del pedido
    pedido.revisado = True
    pedido.enviado = True
    pedido.save()

    return HttpResponseRedirect('/listaPedidos/')

def cancelarPedido(request, id_pedido):
    pedido = OrdenCompra.objects.get(id=id_pedido)
    usuario = pedido.usuario
    
    email_context = {
        'usuario': usuario,
        'pedido': pedido
    }
    # se renderiza el template con el context
    email_html = render_to_string('email_cancelacion.html', email_context)
    # se quitan las etiquetas html para que quede en texto plano
    email_text = strip_tags(email_html)

    send_mail(
        'Cancelación de Pedido',
        email_text,
        'maria.juana.tulua@gmail.com',
        [usuario.email,],
        html_message=email_html,
    )
 
    # se actualiza el estado del pedido
    pedido.revisado = True
    pedido.enviado = False
    pedido.save()

    return HttpResponseRedirect('/listaPedidos/')