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
from core.models import *

#
from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreateForm
#
from django.contrib.auth.forms import AuthenticationForm
#
from django.contrib.auth.decorators import login_required

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
                return redirect('index')
            except:
                return render(request, 'crearcuenta.html', {'form': UserCreateForm, 'error': 'Nombre de usuario ya en uso. Elija a otro nombre de usuario.'})
        else:
            return render(request, 'crearcuenta.html',
                          {'form': UserCreateForm,
                           'error': 'Las contraseñas son diferentes'})

@login_required
def cerrarsesion(request):
    logout(request)
    return redirect('index')


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
            return redirect('index')

def verDrones(request):
    drones = Drone.objects.all()
    return render(request, 'verDrones.html', { 'drones': drones})


def detalleDron(request,dron_id):
    dron = get_object_or_404(Drone, pk=dron_id)
    return render(request, 'detalleDron.html', { 'dron': dron})


def alquilarDron(request,dron_id):
    cliente = request.user  # Obtén el usuario autenticado como cliente
    dron_id = dron_id
    servicio_id = request.POST['servicio']
    fecha_inicio = request.POST['fecha_inicio']
    fecha_fin = request.POST['fecha_fin']
    dron = Drone.objects.get(pk=dron_id)
    servicio = Servicio.objects.get(pk=servicio_id)
        
        # Realiza el cálculo del costo total según tus requerimientos
        # Por ejemplo, aquí asumimos un cálculo simple basado en el precio del servicio y la duración del alquiler
    costo_total = servicio.costo * (fecha_fin - fecha_inicio).days

        # Crea un nuevo registro de alquiler
    alquiler = Alquiler(cliente=cliente, drone=dron, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, servicio=servicio, costo_total=costo_total)
    alquiler.save()

        # Actualiza la disponibilidad del dron
    dron.disponibilidad = False
    dron.save()

def home(request):
    searchTerm = request.GET.get('dron')
    if searchTerm:
        drones = Drone.objects.filter(nombre__icontains=searchTerm)
    else:
        drones = Drone.objects.all()
    return render(request, 'index.html', {'searchTerm': searchTerm, 'drones': drones})


def about(request):
    return render(request, 'about.html')


from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .models import Drone, Alquiler, Servicio
from .forms import DroneForm, AlquilerForm, ServicioForm

class AlquilerDronView(View):
    template_name = 'alquiler.html'

    def get(self, request, dron_id):
        # Obtén el dron basado en el ID proporcionado en la URL
        dron = Drone.objects.get(pk=dron_id)
        drones_disponibles = Drone.objects.filter(disponibilidad=True)
        servicios = Servicio.objects.all()
        drone_form = DroneForm(instance=dron)  # Rellena el formulario con los datos del dron
        alquiler_form = AlquilerForm()
        servicio_form = ServicioForm()
        context = {
            'drones_disponibles': drones_disponibles,
            'servicios': servicios,
            'drone_form': drone_form,
            'alquiler_form': alquiler_form,
            'servicio_form': servicio_form,
            'dron':dron
        }
        return render(request, self.template_name, context)

    def post(self, request, dron_id):
        cliente = request.user
        dron_form = DroneForm(request.POST)
        alquiler_form = AlquilerForm(request.POST)
        servicio_form = ServicioForm(request.POST)

        if dron_form.is_valid() and alquiler_form.is_valid() and servicio_form.is_valid():
            dron = dron_form.save(commit=False)
            servicio = servicio_form.save()
            
            fecha_inicio = alquiler_form.cleaned_data['fecha_inicio']
            fecha_fin = alquiler_form.cleaned_data['fecha_fin']
            costo_total = servicio.costo * (fecha_fin - fecha_inicio).days

            alquiler = alquiler_form.save(commit=False)
            alquiler.cliente = cliente
            alquiler.drone = dron
            alquiler.servicio = servicio
            alquiler.costo_total = costo_total
            alquiler.save()
            
            dron.disponibilidad = False
            dron.save()

            return HttpResponse("Alquiler exitoso. Gracias por usar nuestros servicios.")

        # Si alguno de los formularios no es válido, puedes manejarlo aquí y mostrar los errores.
        # A continuación, puedes volver a renderizar la página con los errores de los formularios.
        drones_disponibles = Drone.objects.filter(disponibilidad=True)
        servicios = Servicio.objects.all()
        context = {
            'drones_disponibles': drones_disponibles,
            'servicios': servicios,
            'drone_form': dron_form,
            'alquiler_form': alquiler_form,
            'servicio_form': servicio_form,
        }
        return render(request, self.template_name, context)
