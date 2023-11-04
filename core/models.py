from django.db import models
from django.contrib.auth.models import User

class Drone(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    modelo = models.CharField(max_length=50)
    autonomia = models.PositiveIntegerField()  # Autonomía de vuelo en minutos
    velocidad_maxima = models.PositiveIntegerField()  # Velocidad máxima en km/h
    carga_maxima = models.PositiveIntegerField()  # Carga máxima en gramos
    disponibilidad = models.BooleanField(default=True)
    precio_hora = models.DecimalField(max_digits=10, decimal_places=2)
    fotografia=models.ImageField(upload_to='images/drones',null=True)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


class Alquiler(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cliente} alquiló {self.drone} del {self.fecha_inicio} al {self.fecha_fin}"





class Tarea(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion_estimada = models.PositiveIntegerField()  # Duración estimada de la tarea en minutos
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    alquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class CoordenadaGPS(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return f"Latitud: {self.latitud}, Longitud: {self.longitud}"
    
class Monitoreo(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    valor = models.FloatField(null=True)
    fotografia=models.ImageField(upload_to='images/foto',null=True)
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f"Monitoreo de {self.tarea} con {self.drone}"

class Comentario(models.Model):
    monitoreo = models.ForeignKey(Monitoreo, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario en {self.monitoreo}: {self.texto}"

