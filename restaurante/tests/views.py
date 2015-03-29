from django.test import TestCase
from restaurante.models import *

class GestionPedidoViewsTestCase(TestCase):
    fixtures = ['restaurante_views_testdata.json', 'user_testdata.json']

    def test_inicio(self):
        resp = self.client.get("/inicio/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('title' in resp.context)
        self.assertEqual(resp.context['title'], 'Inicio')

    def test_servicios(self):
        resp = self.client.get("/servicios/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('title' in resp.context)
        self.assertEqual(resp.context['title'], 'Servicios')

    def test_menu(self):
    	resp = self.client.get("/menu/")
    	self.assertEqual(resp.status_code, 200)
    	self.assertTrue('title' in resp.context)
    	self.assertTrue('categorias_list' in resp.context)
    	self.assertEqual(resp.context['title'], 'Menu')

        categorias = Categoria.objects.all();
        self.assertEqual(len(resp.context['categorias_list']), len(categorias))
        for cat_idx in xrange(0, len(categorias)):
            self.assertEqual(resp.context['categorias_list'][cat_idx].id, categorias[cat_idx].id)

    def test_listaPedidos(self):
        resp = self.client.get("/listaPedidos/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('ordenes' in resp.context)

        ordenes = OrdenCompra.objects.all()
        self.assertEqual(len(resp.context['ordenes']), len(ordenes))
        for ord_idx in xrange(0, len(ordenes)):
            self.assertEqual(resp.context['ordenes'][ord_idx].id, ordenes[ord_idx].id)

    def test_detallePedido(self):
        orden = OrdenCompra.objects.get(id=2)
        resp = self.client.get("/detallePedido/" + str(orden.id))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('ordenCompra' in resp.context)

        self.assertEqual(resp.context['ordenCompra'], orden)

    def test_historialCompra(self):
        self.client.login(username='motas', password='motas') # simulando logueo de usuario 
        resp = self.client.get("/historialCompra/")
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('ordenes' in resp.context)
        ordenes = OrdenCompra.objects.filter(usuario=resp.context['user'])
        self.assertEqual(len(resp.context['ordenes']), len(ordenes))
        for ord_idx in xrange(0, len(ordenes)):
            self.assertEqual(resp.context['ordenes'][ord_idx].id, ordenes[ord_idx].id)

    def test_verCategoria_caso1(self):
    	resp = self.client.get("/verCategoria/1") # Probando que la vista verCategoria con id=1
    	self.assertEqual(resp.status_code, 200)
    	self.assertTrue('title' in resp.context)
    	self.assertTrue('listaProductos' in resp.context)
		
		# Probando que la categoria sea la esperada
    	categoria = Categoria.objects.get(id=1);
    	self.assertEqual(resp.context['title'], categoria.nombre)

    	# Probando que cada producto sea el esperado
    	lista = Producto.objects.filter(tipo=categoria);
    	self.assertEqual(len(resp.context['listaProductos']), len(lista))
    	for prod_idx in xrange(0, len(lista)):
    		self.assertEqual(resp.context['listaProductos'][prod_idx].pk, lista[prod_idx].pk)

    def test_agregarProducto(self):
		User.objects.create_user(username="testUser", password="testPass") # creando usuario de prueba
		self.client.login(username='testUser', password='testPass') # simulando logueo de usuario 
		prod = Producto.objects.get(id=1) # obteniendo el producto a probar
		resp = self.client.get("/agregarProducto/" + str(prod.id)) # agregando el producto 1 al carrito de compra
		self.assertEqual(resp.status_code, 302) # se verifica que haya habido una redireccion codigo 302
		self.assertRedirects(resp, "/verCategoria/" + str(prod.tipo.id)) # despues de que el producto es agregado al carrito de compra, la vista debe redirigir a la categoria del producto 1
		
		session = self.client.session
		self.assertTrue('carrito_compra' in session)  # si todo termino bien, en la variable de sesion debio quedar el carrito de compra
        # obteniendo el carrito,  tener en cuenta que el carrito de compra es un hash map, donde el id del producto es el key, 
		# y el valor es un arreglo, donde la primera posicion es la cantidad
		carrito = session['carrito_compra'] 
		self.assertTrue(carrito.has_key(str(prod.id))) # verificando que el producto con id 1 ha sido insertado a carrito de compra
		# verificando que la cantidad del producto 1 sea 1 porque no existia antes en el carrito de compra
		self.assertEqual(1, carrito[str(prod.id)][0]) 