"""from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

from django.db import models


class Ejercicio(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_subida = models.DateTimeField(auto_now_add=True)
"""
from django.db import models  # importa el módulo models de Django para definir modelos de bases de datos

from django.utils import timezone  # Importa timezone de Django para manejar fechas y horas
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin  # importa clases base
import crypt  # importa la librería crypt para manejar contraseñas

# manager personalizado para el modelo Usuario
class UsuarioManager(BaseUserManager):
    # metodo para crear un usuario
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')  # lanza un error si no hay nombre de usuario
        email = self.normalize_email(email)  
        user = self.model(username=username, email=email, **extra_fields)  # crea una instancia del modelo Usuario
        user.set_password(password)  # establece la contraseña del usuario
        user.save(using=self._db)  # guarda el usuario en la base de datos
        return user

    # Método para crear un superusuario
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # asegura que el superusuario tenga permisos de staff
        extra_fields.setdefault('is_superuser', True)  # asegura que el superusuario tenga permisos de superusuario
        return self.create_user(username, email, password, **extra_fields)  # crea y devuelve el superusuario

# modelo de usuario personalizado
class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)  # campo de nombre de usuario
    email = models.EmailField(unique=True)  # campo de email
    is_maestro = models.BooleanField(default=False)  # campo para indicar si el usuario es maestro
    is_active = models.BooleanField(default=True)  # campo para indicar si el usuario está activo
    is_staff = models.BooleanField(default=False)  # campo para indicar si el usuario es parte del staff

    objects = UsuarioManager()  # Asigna el manager personalizado al modelo

    USERNAME_FIELD = 'username'  # cefine el campo de nombre de usuario
    REQUIRED_FIELDS = ['email']  # cefine los campos obligatorios

    def __str__(self):
        return self.username  # devuelve el nombre de usuario como representación del objeto

# Función para validar contraseñas
def password_valido(pass_a_evaluar: str, shadow: str) -> bool:
    _, algoritmo, salt, resumen = shadow.split('$')  # descompone el valor shadow en sus partes
    configuracion = '$%s$%s$' % (algoritmo, salt)  # crea la configuración para la criptografía
    shadow_nuevo = crypt.crypt(pass_a_evaluar, configuracion)  # genera el hash de la contraseña a evaluar
    return shadow_nuevo == shadow  # compara el hash generado con el hash almacenado

# Modelo de ejercicio
class Ejercicio(models.Model):
    nombre_ejercicio = models.CharField(max_length=200)  # campo para el nombre del ejercicio
    descripcion_ejercicio = models.TextField()  # campo para la descripción del ejercicio
    fecha_entrega = models.DateTimeField(default=timezone.now)  # campo para la fecha de entrega, por defecto la fecha y hora actuales

    def __str__(self):
        return self.nombre_ejercicio  # devuelve el nombre del ejercicio como representación del objeto

# modelo de respuesta a un ejercicio
class RespuestaEjercicio(models.Model):
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)  # campo de clave foránea al modelo Ejercicio
    nombre_alumno = models.CharField(max_length=100)  # campo para el nombre del alumno
    respuesta = models.TextField()  # campo para la respuesta del alumno
    puntaje = models.IntegerField(null=True, blank=True)  # campo para el puntaje, puede ser nulo o estar en blanco

    def __str__(self):
        return self.nombre_alumno  # devuelve el nombre del alumno como representación del objeto

# modelo para registrar intentos fallidos de inicio de sesión
class FailedLoginAttempt(models.Model):
    ip_address = models.GenericIPAddressField()  # Ccmpo para la dirección IP
    attempt_time = models.DateTimeField(auto_now_add=True)  # campo para la hora del intento, se establece automáticamente al crear el registro

    def __str__(self):
        return f"{self.ip_address} - {self.attempt_time}"  # devuelve la dirección IP y la hora del intento como representación del objeto
