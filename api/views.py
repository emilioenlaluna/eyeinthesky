from rest_framework import viewsets
from core.models import Drone, Servicio, Alquiler, CoordenadaGPS, Tarea, Monitoreo, Comentario
from .serializers import DroneSerializer, ServicioSerializer, AlquilerSerializer, CoordenadaGPSSerializer, TareaSerializer, MonitoreoSerializer, ComentarioSerializer

class DroneViewSet(viewsets.ModelViewSet):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    lookup_field = 'id'

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    lookup_field = 'id'

class AlquilerViewSet(viewsets.ModelViewSet):
    queryset = Alquiler.objects.all()
    serializer_class = AlquilerSerializer
    lookup_field = 'id'

class CoordenadaGPSViewSet(viewsets.ModelViewSet):
    queryset = CoordenadaGPS.objects.all()
    serializer_class = CoordenadaGPSSerializer
    lookup_field = 'id'

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    lookup_field = 'id'

class MonitoreoViewSet(viewsets.ModelViewSet):
    queryset = Monitoreo.objects.all()
    serializer_class = MonitoreoSerializer
    lookup_field = 'id'

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    lookup_field = 'id'


