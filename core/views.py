from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
#
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError

#
from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreateForm
#
from django.contrib.auth.forms import AuthenticationForm
#
from django.contrib.auth.decorators import login_required
#
from django.apps import apps
#
from django.shortcuts import get_object_or_404

def crearcuenta(request):
    if request.method == 'GET':
        return render(request, 'crearcuenta.html', {'form': UserCreateForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except:
                return render(request, 'crearcuenta.html', {'form': UserCreateForm, 'error': 'Nombre de usuario ya en uso. Elija a otro nombre de usuario.'})
        else:
            return render(request, 'crearcuenta.html',
                          {'form': UserCreateForm,
                           'error': 'Las contraseñas son diferentes'})

@login_required
def cerrarsesion(request):
    logout(request)
    return redirect('home')


def iniciarsesion(request):
    if request.method == 'GET':
        return render(request, 'iniciarsesion.html', {'form':AuthenticationForm})
    else:
        user = authenticate(request,
        username=request.POST['username'],
        password=request.POST['password']) 
        if user is None:
            return render(request,'iniciarsesion.html',{'form': AuthenticationForm(), 'error': 'Esta cuenta no existe en nuestro registros'})
        else: 
            login(request,user)
            return redirect('home')

@login_required
def verpedidos(request):
    Pedido = apps.get_model(
        app_label='restaurante', model_name='Pedido')
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'vermispedidos.html', { 'pedidos': pedidos})