import os
import django

# Establecer la configuración de Django antes de hacer cualquier otra cosa
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'programacion.settings')
django.setup()

from programacion.models import Usuario  # Importa tu modelo de usuario personalizado

# Asignar un usuario al rol de "Maestro"
username = 'tux'  # Cambia esto por el nombre de usuario real del maestro
try:
    user = Usuario.objects.get(username=username)
    user.is_maestro = True
    user.save()
    print(f"Usuario {username} ha sido asignado como Maestro.")
except Usuario.DoesNotExist:
    print(f"El usuario con nombre de usuario {username} no existe.")
