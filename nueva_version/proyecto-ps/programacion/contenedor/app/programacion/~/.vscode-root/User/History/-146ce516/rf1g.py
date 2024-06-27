from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Usa set_password para almacenar el hash correctamente
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    is_maestro = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username



class RespuestaEjercicio(models.Model):
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    nombre_alumno = models.CharField(max_length=100)
    respuesta = models.TextField()
    codigo_archivo = models.FileField(upload_to='submissions/', null=True, blank=True)  # Asegúrate de tener este campo
    puntaje = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre_alumno

class FailedLoginAttempt(models.Model):
    ip_address = models.GenericIPAddressField()
    attempt_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.attempt_time}"

from django import forms
from .models import Ejercicio

class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre_ejercicio', 'descripcion_ejercicio', 'fecha_entrega']
        widgets = {
            'fecha_entrega': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }