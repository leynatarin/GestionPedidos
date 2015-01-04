from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
	nombre = models.CharField(max_length=30)
	descripcion = models.CharField(max_length=300)
	imagen = models.ImageField(upload_to='menu')
	enlaceHtml = models.CharField(max_length=100)

	def __unicode__(self):
		return self.nombre

class Ingrediente(models.Model):
	nombre = models.CharField(max_length=140)

	def __unicode__(self):
		return self.nombre

class Producto(models.Model):
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=500)
	precio = models.FloatField()
	iva = models.FloatField()
	imagen = models.ImageField(upload_to='productos/entradas')
	tipo = models.ForeignKey(Categoria)
	codigo = models.IntegerField()
	ingredientes = models.ManyToManyField(Ingrediente)
	
	def __unicode__(self):
		return self.nombre

class OrdenCompra(models.Model):
	usuario = models.ForeignKey(User)
	productos = models.ManyToManyField(Producto, through='OrdenProducto')
	total = models.FloatField()
	impuestos = models.FloatField()
	fecha = models.DateField()
	revisado = models.BooleanField(default=False)
	enviado = models.BooleanField(default=False)

class OrdenProducto(models.Model):
	producto = models.ForeignKey(Producto)
	ordenCompra = models.ForeignKey(OrdenCompra)
	cantidad = models.IntegerField()