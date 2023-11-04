from django.http import HttpResponseRedirect
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
from django.urls import reverse
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
from .models import Drone, Servicio, Alquiler
from django.contrib.auth.decorators import login_required

@login_required
def crear_alquiler(request, dron_id):
    # Obtén el dron basado en el ID pasado en la URL
    dron = Drone.objects.get(id=dron_id)

    if request.method == "POST":
        # Obtén los datos del formulario
        cliente = request.user
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        servicio_id = request.POST.get("servicio")

        # Obtiene el servicio seleccionado
        servicio = Servicio.objects.get(id=servicio_id)

        # Calcula el costo total del alquiler
        # Aquí asumimos que el costo total se calcula en función de la duración del alquiler y el precio del servicio
        costo_total = calcular_costo_total(fecha_inicio, fecha_fin, servicio)

        # Crea un nuevo objeto Alquiler
        alquiler = Alquiler(
            cliente=cliente,
            drone=dron,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            servicio=servicio,
            costo_total=costo_total,
        )

        # Guarda el alquiler en la base de datos
        alquiler.save()

        # Redirecciona a una página de éxito o a donde desees
        return HttpResponseRedirect(reverse('pagina_de_exito', args=[alquiler.id]))

    else:
        # Obtiene la lista de servicios existentes
        servicios = Servicio.objects.all()

        return render(request, 'alquiler.html', {
            'dron': dron,
            'servicios': servicios,
        })

from datetime import datetime

def calcular_costo_total(fecha_inicio, fecha_fin, servicio):
    # Convierte las cadenas de fecha en objetos de fecha
    fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

    # Calcula la diferencia en días
    diferencia_fechas = fecha_fin - fecha_inicio

    # Calcula el costo total en función de la duración y el precio del servicio
    costo_total = diferencia_fechas.days * servicio.costo
    return costo_total


def pagina_de_exito(request, alquiler_id):
    alquiler = Alquiler.objects.get(id=alquiler_id)
    return render(request, 'pagina_exito.html', {'alquiler': alquiler})

@login_required
def mis_alquileres(request):
    # Obtiene los alquileres del usuario actual
    alquileres = Alquiler.objects.filter(cliente=request.user)

    return render(request, 'mis_alquileres.html', {'alquileres': alquileres})

from django.shortcuts import render, redirect
from .models import Alquiler, Tarea, CoordenadaGPS
from django.contrib.auth.decorators import login_required

@login_required
def agregar_tarea(request, alquiler_id):
    # Obtén el alquiler basado en el ID pasado en la URL
    alquiler = Alquiler.objects.get(id=alquiler_id)

    if request.method == "POST":
        # Obtén los datos del formulario
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
       
        duracion_estimada = request.POST.get("duracion_estimada")
        costo = request.POST.get("costo")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")

       
        # Crea un nuevo objeto Tarea
        tarea = Tarea(
            nombre=nombre,
            descripcion=descripcion,
            duracion_estimada=duracion_estimada,
            costo=0,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            alquiler=alquiler,
        )

        tarea.save()

        # Asigna las coordenadas seleccionadas a la tarea
        

        return redirect('detalle_alquiler', alquiler_id=alquiler.id)

    else:
        # Obtiene las coordenadas disponibles
        coordenadas = CoordenadaGPS.objects.all()

        return render(request, 'agregar_tarea.html', {
            'alquiler': alquiler,
            'coordenadas': coordenadas,
        })


@login_required
def detalle_alquiler(request, alquiler_id):
    # Obtén el alquiler basado en el ID pasado en la URL
    alquiler = Alquiler.objects.get(id=alquiler_id)

    # Obtiene las tareas relacionadas con el alquiler
    tareas = Tarea.objects.filter(alquiler=alquiler)

    return render(request, 'detalle_alquiler.html', {'alquiler': alquiler, 'tareas': tareas})

from django.shortcuts import render, redirect
from .models import Tarea, CoordenadaGPS
from django.contrib.auth.decorators import login_required

@login_required
def agregar_coordenadas(request, tarea_id):
    # Obtén la tarea basada en el ID pasado en la URL
    tarea = Tarea.objects.get(id=tarea_id)

    if request.method == "POST":
        # Obtén los datos del formulario
        latitud = request.POST.get("latitud")
        longitud = request.POST.get("longitud")

        # Crea un nuevo objeto CoordenadaGPS
        coordenada = CoordenadaGPS(latitud=latitud, longitud=longitud,tarea=tarea)
        coordenada.save()


        return redirect('detalle_tarea', alquiler_id=tarea.id)


    return render(request, 'agregar_coordenadas.html', {'tarea': tarea})


from django.shortcuts import render, get_object_or_404
from .models import Tarea

def detalle_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id)
    coordenadas = CoordenadaGPS.objects.filter(tarea=tarea)
    
    return render(request, 'detalle_tarea.html', {'tarea': tarea, 'coordenadas': coordenadas})

from core.models import Log

from django.db.models import OuterRef, Subquery

def detalle_log(request):

  current_user = request.user

  drones = Drone.objects.filter(id__in=Subquery(
    Log.objects.filter(user=current_user).values('drone__id')
  ))

  context = {
    'drones': []  
  }

  for drone in drones:
    logs = Log.objects.filter(user=current_user,drone=drone).order_by('-timestep')
    context['drones'].append({
      'drone': drone,
      'logs': logs
    })

  return render(request, 'detalle_log.html', context)