# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.core.files.images import get_image_dimensions

class Perfil(models.Model):
    user      = models.OneToOneField(User, unique=True, related_name='perfil')
    telefono  = models.PositiveIntegerField()
    direccion = models.TextField(max_length=1024)
    barrio    = models.TextField(max_length=1024)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __unicode__(self):
        return self.user.username

class FormularioRegistro(ModelForm):
    class Meta:
        model   = User
        fields  = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder':'Nombre de usuario', 'id':'nombre', 'name':'nombre', 'maxlength':'100','class':''}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'id':'contraseña', 'name':'contraseña', 'maxlength':'100','class':''}),
            'email': forms.EmailInput(attrs={'placeholder':'E-Mail', 'id':'e-mail', 'name':'e-mail', 'maxlength':'100','class':''}),
            'first_name': forms.TextInput(attrs={'placeholder':'Nombre', 'id':'primNombre', 'name':'primNombre', 'maxlength':'100','class':''}),
            'last_name': forms.TextInput(attrs={'placeholder':'Apellidos', 'id':'apellido', 'name':'apellido', 'maxlength':'100','class':''}),
        }

class FormularioRegistroPerfil(ModelForm):
    class Meta:
        model   = Perfil
        fields  = [ 'avatar', 'telefono', 'direccion', 'barrio' ]
        widgets = {
            'avatar': forms.FileInput(attrs={'id':'avatar', 'name':'avatar', 'maxlength':'100','class':'span8'}),
            'telefono': forms.TextInput(attrs={'placeholder':'Teléfono o Celular', 'id':'telefono', 'name':'telefono', 'maxlength':'100','class':''}),
            'direccion': forms.TextInput(attrs={'placeholder':'Dirección' , 'id':'direccion', 'name':'direccion', 'maxlength':'100','class':''}),
            'barrio': forms.TextInput(attrs={'placeholder':'Barrio', 'id':'barrio', 'name':'barrio', 'maxlength':'100','class':''}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        
        if (avatar):
            try:
                w, h = get_image_dimensions(avatar)
                #validate dimensions
                max_width = max_height = 350
                if w > max_width or h > max_height:
                    raise forms.ValidationError(
                        u'Please use an image that is '
                         '%s x %s pixels or smaller.' % (max_width, max_height))
                    
                #validate content type
                main, sub = avatar.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png', 'jpg']):
                    raise forms.ValidationError(u'Please use a JPEG, '
                        'GIF or PNG image.')
                    
                #validate file size
                if len(avatar) > (20 * 1024):
                    raise forms.ValidationError(
                        u'Avatar file size may not exceed 20k.')
                    
            except AttributeError:
                """
                Handles case when we are updating the user profile
                and do not supply a new avatar
                """
                pass
            
        return avatar