# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

class Perfil(models.Model):
    user      = models.OneToOneField(User, unique=True, related_name='perfil')
    telefono  = models.PositiveIntegerField()
    direccion = models.TextField(max_length=1024)
    barrio    = models.TextField(max_length=1024)

    def __unicode__(self):
        return self.user.username

class FormularioRegistro(ModelForm):
    class Meta:
        model   = User
        fields  = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder':'Nombre de usuario', 'id':'nombre', 'name':'nombre', 'size':'20','maxlength':'100','class':'span8'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'id':'contraseña', 'name':'contraseña', 'size':'20','maxlength':'100','class':'span8'}),
            'email': forms.EmailInput(attrs={'placeholder':'E-Mail', 'id':'e-mail', 'name':'e-mail', 'size':'20','maxlength':'100','class':'span8'}),
            'first_name': forms.TextInput(attrs={'placeholder':'Nombre', 'id':'primNombre', 'name':'primNombre', 'size':'20','maxlength':'100','class':'span8'}),
            'last_name': forms.TextInput(attrs={'placeholder':'Apellidos', 'id':'apellido', 'name':'apellido', 'size':'20','maxlength':'100','class':'span8'}),
        }

class FormularioRegistroPerfil(ModelForm):
    class Meta:
        model   = Perfil
        fields  = [ 'telefono', 'direccion', 'barrio' ]
        widgets = {
            'telefono': forms.TextInput(attrs={'placeholder':'Teléfono o Celular', 'id':'telefono', 'name':'telefono', 'size':'20','maxlength':'100','class':'span8'}),
            'direccion': forms.TextInput(attrs={'placeholder':'Dirección' , 'id':'direccion', 'name':'direccion', 'size':'20','maxlength':'100','class':'span8'}),
            'barrio': forms.TextInput(attrs={'placeholder':'Barrio', 'id':'barrio', 'name':'barrio', 'size':'20','maxlength':'100','class':'span8'}),
        }