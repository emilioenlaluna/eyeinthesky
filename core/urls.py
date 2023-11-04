from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="index"),
    path("about", views.about, name="about"),
    path("login", views.iniciarsesion, name="login"),
    path("register", views.crearcuenta, name="register"),
    path("logout", views.cerrarsesion, name="logout"),
    path("verDrones", views.verDrones, name="verDrones"),
    path("detalleDron/<int:dron_id>", views.detalleDron, name="detalleDron"), 
    path('crear_alquiler/<int:dron_id>/', views.crear_alquiler, name='crear_alquiler'),
    path('pagina_exito/<int:alquiler_id>/', views.pagina_de_exito, name='pagina_de_exito'),
path('mis_alquileres/', views.mis_alquileres, name='mis_alquileres'),

path('agregar_tarea/<int:alquiler_id>/', views.agregar_tarea, name='agregar_tarea'),
path('detalle_alquiler/<int:alquiler_id>/', views.detalle_alquiler, name='detalle_alquiler'),
path('agregar_coordenadas/<int:tarea_id>/', views.agregar_coordenadas, name='agregar_coordenadas'),
 path('detalle_tarea/<int:tarea_id>/', views.detalle_tarea, name='detalle_tarea'),
]