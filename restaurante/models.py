from django.db import models
from django.contrib.auth.models import User
from recommends.providers import recommendation_registry, RecommendationProvider

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

class ProductRecommendationProvider(RecommendationProvider):
    def get_users(self):
        return User.objects.filter(is_active=True).distinct()

    def get_items(self):
        return Product.objects.all()

    def get_ratings(self, obj):
        return OrdenProducto.objects.filter(product=obj)

    def get_rating_score(self, rating):
        return rating.cantidad

    def get_rating_user(self, rating):
        return rating.ordenCompra.usuario

    def get_rating_item(self, rating):
    	return rating.producto

    def get_rating_site(self, rating):
        return Site.objects.get_current()

recommendation_registry.register(OrdenProducto, [Producto], ProductRecommendationProvider)