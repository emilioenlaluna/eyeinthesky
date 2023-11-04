from rest_framework import serializers
from core.models import Drone, Servicio, Alquiler, CoordenadaGPS, Tarea, Monitoreo, Comentario

class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class AlquilerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alquiler
        fields = '__all__'

class CoordenadaGPSSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoordenadaGPS
        fields = '__all__'

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'

class MonitoreoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitoreo
        fields = '__all__'

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'

