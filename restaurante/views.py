from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from recommends.tasks import recommends_precompute
from .models import *
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
    else:
        result = {'title': 'Carrito de Compra', 'total': 0, 'impuestos': 0, "carrito": {}}
    return render_to_response('carritoCompra.html', result, context_instance=RequestContext(request))

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

def listaPedidos(request):
    ordenes = OrdenCompra.objects.all()
    return render_to_response('listaPedidos.html', {'ordenes': ordenes}, context_instance=RequestContext(request))

def detallePedido(request, id):
    orden = OrdenCompra.objects.get(id=id)
    return render_to_response('detallePedido.html', {'ordenCompra': orden}, context_instance=RequestContext(request))

def historialCompra(request):
    ordenes = OrdenCompra.objects.filter(usuario=request.user)
    return render_to_response('historialCompra.html', {'ordenes': ordenes}, context_instance=RequestContext(request))