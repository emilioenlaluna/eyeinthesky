from django.contrib.auth.forms import UserCreationForm
from django.forms import forms
from django import forms
from django.forms import ModelForm, CharField,IntegerField
from core.models import *

class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args,**kwargs)
        for fieldname in ['username', 'password1','password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'})

from django import forms
from django.core.exceptions import ValidationError
from .models import Drone, Alquiler, Servicio

class DroneForm(forms.ModelForm):
    class Meta:
        model = Drone
        fields = ['nombre', 'descripcion', 'modelo', 'autonomia', 'velocidad_maxima', 'carga_maxima', 'disponibilidad', 'precio_hora', 'fotografia']

class AlquilerForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = ['cliente', 'drone', 'fecha_inicio', 'fecha_fin', 'servicio', 'costo_total']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'costo']
