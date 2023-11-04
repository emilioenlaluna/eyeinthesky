from django.urls import path, include
from rest_framework import routers
from . import views

# Crea un router
router = routers.DefaultRouter()

# Registra los ViewSets para los modelos existentes
router.register(r'drones', views.DroneViewSet)
router.register(r'servicios', views.ServicioViewSet)
router.register(r'alquileres', views.AlquilerViewSet)
router.register(r'coordenadasgps', views.CoordenadaGPSViewSet)
router.register(r'tareas', views.TareaViewSet)
router.register(r'monitoreos', views.MonitoreoViewSet)
router.register(r'comentarios', views.ComentarioViewSet)

# Define las URL de la API
urlpatterns = [
    path('', include(router.urls)),
]
