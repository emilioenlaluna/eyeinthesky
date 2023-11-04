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

admin.site.site_header = "Eye in the sky"
admin.site.site_title = "Eye in the sky / Emprende Uaa 2023"
admin.site.index_title = "Bienvenido al Eye in the sky Portal"