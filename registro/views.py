from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from registro.models import FormularioRegistro, FormularioRegistroPerfil, Perfil

def registro(request):
    if request.method == 'POST':  # If the form has been submitted...
        userForm = FormularioRegistro(request.POST)  # A form bound to the POST data
        perfilForm = FormularioRegistroPerfil(request.POST, request.FILES)
        if userForm.is_valid() and perfilForm.is_valid():  # All validation rules pass

            # Process the data in form.cleaned_data
            username   = userForm.cleaned_data["username"]
            password   = userForm.cleaned_data["password"]
            email      = userForm.cleaned_data["email"]
            first_name = userForm.cleaned_data["first_name"]
            last_name  = userForm.cleaned_data["last_name"]

            telefono  = perfilForm.cleaned_data["telefono"]
            direccion = perfilForm.cleaned_data["direccion"]
            barrio    = perfilForm.cleaned_data["barrio"]

            # At this point, user is a User object that has already been saved
            # to the database. You can continue to change its attributes
            # if you want to change other fields.
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name

            perfil = Perfil.objects.create(user=user, telefono=telefono, direccion=direccion, barrio=barrio)

            # Save new user attributes
            user.save()
            perfil.save()

            email_context = {
                'usuario': user,
            }
            # se renderiza el template con el context
            email_html = render_to_string('confirmacion_registro_email.html', email_context)
            # se quitan las etiquetas html para que quede en texto plano
            email_text = strip_tags(email_html)

            send_mail(
                'Confirmacion de Registro',
                email_text,
                'maria.juana.tulua@gmail.com',
                [user.email,],
                html_message=email_html,
            )
            return HttpResponseRedirect('/menu')  # Redirect after POST
    else:
        userForm = FormularioRegistro()
        perfilForm = FormularioRegistroPerfil()

    data = {
        'userForm': userForm,
        'perfilForm': perfilForm,
    }
    return render_to_response('registro.html', data, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def editarPerfil(request):
    usuario = User.objects.get(id=request.user.id)
    perfil = Perfil.objects.get(user=usuario)
    mensaje = ""

    if request.method == 'POST':  # If the form has been submitted...
        userForm = FormularioRegistro(request.POST, instance=usuario)  # A form bound to the POST data
        perfilForm = FormularioRegistroPerfil(request.POST, instance=perfil)
        if perfilForm.is_valid():  # All validation rules pass

            if not userForm["email"].errors:
                usuario.email = userForm.cleaned_data["email"]

            if not userForm["first_name"].errors:
                usuario.first_name = userForm.cleaned_data["first_name"]

            if not userForm["last_name"].errors:
                usuario.last_name = userForm.cleaned_data["last_name"]

            if not perfilForm["telefono"].errors:
                perfil.telefono = perfilForm.cleaned_data["telefono"]

            if not perfilForm["direccion"].errors:
                perfil.direccion = perfilForm.cleaned_data["direccion"]

            if not perfilForm["barrio"].errors:
                perfil.barrio = perfilForm.cleaned_data["barrio"]

            # Save new user attributes
            usuario.save()
            perfil.save()
            mensaje = "Sus datos han sido actualizados exitosamente"

            # return render_to_response('menu.html')  # Redirect after POST
    
    userForm = FormularioRegistro(instance=usuario)
    perfilForm = FormularioRegistroPerfil(instance=perfil)

    data = {
        'userForm': userForm,
        'perfilForm': perfilForm,
        'mensaje': mensaje
    }
    return render_to_response('editarPerfil.html', data, context_instance=RequestContext(request))