from django.contrib import admin
from .models import *

# Register your models here.
admin.register(Drone)
admin.register(Servicio)
admin.register(Alquiler)
admin.register(CoordenadaGPS)
admin.register(Tarea)
admin.register(Monitoreo)
admin.register(Comentario)