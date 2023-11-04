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
    path('alquilarDron/<int:dron_id>/', views.AlquilerDronView.as_view(), name='alquilarDron'),
]