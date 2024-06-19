from django.contrib import admin
from .models import Usuario




from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Usuario, Ejercicio, RespuestaEjercicio

# Registrar tus modelos
admin.site.register(Usuario)
admin.site.register(Ejercicio)
admin.site.register(RespuestaEjercicio)

# Evitar registrar el modelo Group si ya está registrado
try:
    admin.site.register(Group)
except admin.sites.AlreadyRegistered:
    pass

