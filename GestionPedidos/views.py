from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from restaurante.models import *
import datetime

def inicio(request):
	return render_to_response('inicio.html', {'title': 'Inicio'}, context_instance=RequestContext(request))

def servicios(request):
	return render_to_response('servicios.html', {'title': 'Servicios'}, context_instance=RequestContext(request))

def menu(request):
	categorias = Categoria.objects.all();
	return render_to_response('menu.html', {'title': 'Menu', 'categorias_list': categorias}, context_instance=RequestContext(request))

def entradas(request):
	entradas_list = Producto.objects.filter(tipo__nombre="Entradas");
	return render_to_response('entradas.html', {'title': 'Entradas', 'entradas': entradas_list}, context_instance=RequestContext(request))

def menuInfantil(request):
	infantil = Producto.objects.filter(tipo__nombre="Menu Infantil");
	return render_to_response('menuInfantil.html', {'title': 'menu Infantil', 'menuInfantil': infantil}, context_instance=RequestContext(request))

def perrosCalientes(request):
	perros = Producto.objects.filter(tipo__nombre="Perros Calientes");
	return render_to_response('perrosCalientes.html', {'title': 'Perros Calientes', 'perrosCalientes': perros}, context_instance=RequestContext(request))

def hamburguesas(request):
	hamburguesas = Producto.objects.filter(tipo__nombre="Hamburguesas");
	return render_to_response('hamburguesas.html', {'title': 'Hamburguesas', 'hamburguesas': hamburguesas}, context_instance=RequestContext(request))

def parrilla(request):
	parrilla = Producto.objects.filter(tipo__nombre="Parrilla");
	return render_to_response('parrilla.html', {'title': 'Parrilla', 'parrilla': parrilla}, context_instance=RequestContext(request))

def pescados(request):
	pescados = Producto.objects.filter(tipo__nombre="Pescados");
	return render_to_response('pescados.html', {'title': 'Pescados', 'pescados': pescados}, context_instance=RequestContext(request))

def sandwich(request):
	sandwich = Producto.objects.filter(tipo__nombre="Sandwich");
	return render_to_response('sandwich.html', {'title': 'Sandwich', 'sandwich': sandwich}, context_instance=RequestContext(request))

def salchipapas(request):
	salchipapas = Producto.objects.filter(tipo__nombre="Salchipapas");
	return render_to_response('salchipapas.html', {'title': 'Salchipapas', 'salchipapas': salchipapas}, context_instance=RequestContext(request))

def tostadas(request):
	tostadas = Producto.objects.filter(tipo__nombre="Tostadas");
	return render_to_response('tostadas.html', {'title': 'Tostadas', 'tostadas': tostadas}, context_instance=RequestContext(request))

def ensaladas(request):
	ensaladas = Producto.objects.filter(tipo__nombre="Ensaladas");
	return render_to_response('ensaladas.html', {'title': 'Ensaladas', 'ensaladas': ensaladas}, context_instance=RequestContext(request))

def desgranados(request):
	desgranados = Producto.objects.filter(tipo__nombre="Desgranados");
	return render_to_response('desgranados.html', {'title': 'Desgranados', 'desgranados': desgranados}, context_instance=RequestContext(request))

def bebidas(request):
	bebidas = Producto.objects.filter(tipo__nombre="Bebidas");
	return render_to_response('bebidas.html', {'title': 'Bebidas', 'bebidas': bebidas}, context_instance=RequestContext(request))

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

	return HttpResponseRedirect("/" + product.tipo.enlaceHtml)

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
		return render_to_response('confirmacionPedido.html', context_instance=RequestContext(request))

def confirmacionPedido(request):
	return render_to_response('confirmacionPedido.html', context_instance=RequestContext(request))

def listaPedidos(request):
	ordenes = OrdenCompra.objects.all()
	return render_to_response('listaPedidos.html', {'ordenes': ordenes}, context_instance=RequestContext(request))

def detallePedido(request, id):
	orden = OrdenCompra.objects.get(id=id)
	return render_to_response('detallePedido.html', {'ordenCompra': orden}, context_instance=RequestContext(request))
