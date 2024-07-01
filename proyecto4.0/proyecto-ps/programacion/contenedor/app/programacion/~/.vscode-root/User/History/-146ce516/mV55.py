from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
"""""
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
        """


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    is_maestro = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    bot_id = models.CharField(max_length=100, blank=True, null=True)  # Nuevo campo para bot_id
    chat_id = models.CharField(max_length=100, blank=True, null=True)  # Nuevo campo para chat_id

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    

    
from django.db import models

class Ejercicio(models.Model):
    nombre_ejercicio = models.CharField(max_length=255)
    descripcion_ejercicio = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_entrega = models.DateTimeField()
    casos_de_prueba = models.TextField()

    def __str__(self):
        return self.nombre_ejercicio
    


from django.utils import timezone

class RespuestaEjercicio(models.Model):
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    nombre_alumno = models.CharField(max_length=100)
    respuesta = models.TextField()
    codigo_archivo = models.FileField(upload_to='submissions/', null=True, blank=True)
    puntaje = models.IntegerField(null=True, blank=True)
    fecha_subida = models.DateTimeField(default=timezone.now)  # Define un valor predeterminado

    def __str__(self):
        return self.nombre_alumno


class FailedLoginAttempt(models.Model):
    ip_address = models.GenericIPAddressField()
    attempt_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.attempt_time}"
