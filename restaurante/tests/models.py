from django.test import TestCase
from restaurante.models import *

class RestauranteModelsTestCase(TestCase):

    def test_Categoria(self):
        nombre = "Categoria"
        descripcion = "Descrpcion"
        imagen = "imagen/categoria.png"
        enlaceHtml = "categoria"
       
        categoria = Categoria.objects.create(nombre=nombre, descripcion=descripcion, imagen=imagen, enlaceHtml=enlaceHtml)
        self.assertEquals(nombre, unicode(categoria))

  