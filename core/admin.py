from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Drone)
admin.site.register(Servicio)
admin.site.register(Alquiler)
admin.site.register(CoordenadaGPS)
admin.site.register(Tarea)
admin.site.register(Monitoreo)
admin.site.register(Comentario)

admin.site.site_header = "Eye in the sky"
admin.site.site_title = "Eye in the sky / Emprende Uaa 2023"
admin.site.index_title = "Bienvenido al Eye in the sky Portal"