from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from .telegram import enviar_mensaje
from .forms import CodigoAccesoForm, UsuarioForm, EjercicioForm, RespuestaEjercicioForm
from .models import Usuario, Ejercicio, FailedLoginAttempt, RespuestaEjercicio
import crypt
import string
import datetime
import random
from .forms import LoginForm
from .models import Usuario, FailedLoginAttempt
# /code/programacion/views.py

def index(request):
    return HttpResponse("<h1>Hola Mundo</h1>")

def password_valido(pass_a_evaluar: str, shadow: str) -> bool:
    _, algoritmo, salt, resumen = shadow.split('$')
    configuracion = '$%s$%s$' % (algoritmo, salt)
    shadow_nuevo = crypt.crypt(pass_a_evaluar, configuracion)
    return shadow_nuevo == shadow

# views.py
from django.conf import settings

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            ip_address = request.META.get('REMOTE_ADDR')
            now = timezone.now()
            attempt_limit = 5
            lockout_time = datetime.timedelta(seconds=60)

            recent_attempts = FailedLoginAttempt.objects.filter(
                ip_address=ip_address,
                attempt_time__gt=now - lockout_time
            )

            if recent_attempts.count() >= attempt_limit:
                messages.error(request, f"Has alcanzado el límite de intentos. Intenta nuevamente en {lockout_time.seconds} segundos.")
                return render(request, 'login.html', {'form': form})

            try:
                user = Usuario.objects.get(username=username)
                if password_valido(password, user.password):
                    auth_logout(request)  # Invalida cualquier sesión existente
                    FailedLoginAttempt.objects.filter(ip_address=ip_address).delete()
                    
                    # Aquí es donde configuramos un nombre de cookie de sesión único si es necesario
                    if user.is_maestro:
                        request.session['is_maestro'] = True
                        settings.SESSION_COOKIE_NAME = 'maestro_sessionid'
                    else:
                        request.session['is_maestro'] = False
                        settings.SESSION_COOKIE_NAME = 'alumno_sessionid'

                    auth_login(request, user)  # Inicia la sesión del usuario

                    next_url = request.POST.get('next')
                    if not next_url:
                        next_url = '/autenticacion/'

                    return redirect(next_url)
                else:
                    FailedLoginAttempt.objects.create(ip_address=ip_address)
                    messages.error(request, 'Nombre de usuario o contraseña incorrectos')
            except Usuario.DoesNotExist:
                FailedLoginAttempt.objects.create(ip_address=ip_address)
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Error en el formulario. Verifica los datos e intenta de nuevo.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'next': request.GET.get('next', '')})


"""
def registro(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_exitoso')
    else:
        form = UsuarioForm()
    return render(request, 'registro.html', {'form': form})
    """


# views.py
def registro(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UsuarioForm()
    return render(request, 'registro.html', {'form': form})


def registro_exitoso(request):
    return render(request, 'login.html')

def generar_codigo_verificacion(length=8):
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(random.choice(caracteres) for i in range(length))
    return codigo
"""
@login_required
def autenticacion(request):
    if request.method == 'POST':
        codigo_verificacion = generar_codigo_verificacion()
        mensaje = f'Su código de verificación es: {codigo_verificacion}'

        if enviar_mensaje(mensaje):
            request.session['codigo_correcto'] = codigo_verificacion
            request.session['codigo_generado'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return redirect('ingresar_codigo_acceso')
        else:
            return HttpResponse('Hubo un error al enviar el código de verificación.')
    return render(request, 'autenticacion.html')
    """
from .telegram import enviar_mensaje, generar_codigo_verificacion

@login_required
def autenticacion(request):
    if request.method == 'POST':
        user = request.user
        codigo_verificacion = generar_codigo_verificacion()
        mensaje = f'Su código de verificación es: {codigo_verificacion}'
        
        if enviar_mensaje(mensaje, user.bot_id, user.chat_id):
            request.session['codigo_correcto'] = codigo_verificacion
            request.session['codigo_generado'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return redirect('ingresar_codigo_acceso')
        else:
            return HttpResponse('Hubo un error al enviar el código de verificación.')
    return render(request, 'autenticacion.html')



@login_required
def ingresar_codigo_acceso(request):
    if request.method == 'POST':
        form = CodigoAccesoForm(request.POST)
        if form.is_valid():
            codigo_ingresado = form.cleaned_data['codigo_acceso']
            codigo_correcto = request.session.get('codigo_correcto')
            codigo_generado = request.session.get('codigo_generado')

            if not codigo_correcto or not codigo_generado:
                messages.error(request, "Intento de reutilización del código detectado. Por favor, solicita un nuevo código.")
                return redirect('login')

            if codigo_correcto and codigo_generado:
                codigo_generado_dt = datetime.datetime.strptime(codigo_generado, '%Y-%m-%d %H:%M:%S')
                tiempo_transcurrido = datetime.datetime.now() - codigo_generado_dt
                tiempo_maximo = datetime.timedelta(minutes=3)

                if tiempo_transcurrido > tiempo_maximo:
                    messages.error(request, "El código ha expirado. Por favor, solicita un nuevo código.")
                    return redirect('login')
                elif codigo_ingresado == codigo_correcto:
                    if request.user.is_maestro:
                        return redirect('menu_maestro')
                    else:
                        return redirect('menu_alumno')
                else:
                    messages.error(request, "Código de acceso incorrecto. Por favor, inténtalo de nuevo.")
                    return redirect('login')
    else:
        form = CodigoAccesoForm()

    return render(request, 'ingresar_codigo_acceso.html', {'form': form})


@login_required
def ver_respuestas(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)
    respuestas = RespuestaEjercicio.objects.filter(ejercicio=ejercicio)
    return render(request, 'ver_respuestas.html', {'respuestas': respuestas, 'ejercicio': ejercicio})

def es_maestro(user):
    return user.is_maestro

@login_required
@user_passes_test(lambda u: not u.is_maestro)
def menu_alumno(request):
    ejercicios = Ejercicio.objects.all()
    mensaje_fecha_pasada = None

    if request.method == 'GET' and 'ejercicio_id' in request.GET:
        ejercicio_id = request.GET['ejercicio_id']
        ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)
        if datetime.now() > ejercicio.fecha_entrega:
            mensaje_fecha_pasada = f"La fecha de entrega ha pasado para el ejercicio {ejercicio.nombre_ejercicio}. No puedes subir respuestas."

    return render(request, 'menu_alumno.html', {
        'ejercicios': ejercicios,
        'mensaje_fecha_pasada': mensaje_fecha_pasada,
    }

@login_required
@user_passes_test(es_maestro)
def menu_maestro(request):
    if not request.session.get('is_maestro', True):
        raise PermissionDenied("Acceso denegado para alumnos.")
    ejercicios = Ejercicio.objects.all()
    respuestas = RespuestaEjercicio.objects.all()
    return render(request, 'menu_maestro.html', {'ejercicios': ejercicios, 'respuestas': respuestas})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from .forms import EjercicioForm


import os
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib import messages

@login_required
@user_passes_test(lambda u: u.is_maestro)
def crear_ejercicio(request):
    if request.method == 'POST':
        form = EjercicioForm(request.POST)
        if form.is_valid():
            ejercicio = form.save()
            casos_de_prueba_path = f'/tmp/casos_de_prueba_{ejercicio.id}.txt'
            with open(casos_de_prueba_path, 'w') as f:
                f.write(ejercicio.casos_de_prueba)
            
            # Comando para copiar el archivo al contenedor executor
            command = f'docker cp {casos_de_prueba_path} programacion_executor_1:/code/test_case/casos_de_prueba_{ejercicio.id}.txt'
            os.system(command)

            # Eliminar el archivo temporal
            os.remove(casos_de_prueba_path)

            messages.success(request, 'El ejercicio se ha creado exitosamente.')
            return redirect('crear_ejercicio')
        else:
            messages.error(request, 'Error al crear el ejercicio. Por favor, verifica los datos e intenta de nuevo.')
    else:
        form = EjercicioForm()
    return render(request, 'crear_ejercicio.html', {'form': form})


@login_required
def listar_ejercicios(request):
    ejercicios = Ejercicio.objects.all()
    return render(request, 'listar_ejercicios.html', {'ejercicios': ejercicios})

@login_required
def detalle_ejercicio(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)
    puntaje = request.GET.get('puntaje')
    return render(request, 'detalle_ejercicio.html', {'ejercicio': ejercicio, 'puntaje': puntaje})

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from .telegram import enviar_mensaje
from .forms import CodigoAccesoForm, UsuarioForm, EjercicioForm, RespuestaEjercicioForm
from .models import Usuario, Ejercicio, FailedLoginAttempt, RespuestaEjercicio
import crypt
import string
import datetime
import random
import subprocess
import os
import json
import sys
import os
import subprocess
import json
import logging
from queue import Queue
from threading import Thread
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ejercicio, RespuestaEjercicio
from .forms import RespuestaEjercicioForm
from .scripts import analizar_codigo

# Configuración de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Inicialización de la cola de tareas
task_queue = Queue()

# Definición del worker para procesar las tareas de la cola
def worker():
    while True:
        task = task_queue.get()
        if task is None:
            break
        code_path, casos_path, respuesta_id = task
        logger.debug(f"Procesando tarea: {task}")
        try:
            result = evaluar_con_casos_directos(code_path, casos_path)
            puntaje = calcular_puntaje(result)
            actualizar_puntaje_respuesta(respuesta_id, puntaje)
            logger.info(f"Tarea {respuesta_id} procesada exitosamente. Puntaje: {puntaje}")
        except Exception as e:
            logger.error(f"Error al procesar la tarea {respuesta_id}: {e}")
        task_queue.task_done()

# Inicializar el hilo del worker
Thread(target=worker, daemon=True).start()

# Función para añadir tareas a la cola
def add_task_to_queue(code_path, casos_path, respuesta_id):
    task_queue.put((code_path, casos_path, respuesta_id))
    return respuesta_id

# Función para actualizar el puntaje de la respuesta
def actualizar_puntaje_respuesta(respuesta_id, puntaje):
    respuesta = RespuestaEjercicio.objects.get(id=respuesta_id)
    respuesta.puntaje = puntaje
    respuesta.save()

# Función para evaluar con casos de prueba directos
def evaluar_con_casos_directos(code_path, casos_path):
    comando = f"docker exec -i programacion-programacion-executor-1-1 python3 /code/programacion/scripts/scripts.py {code_path} {casos_path}"
    result = subprocess.run(comando, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"Error al ejecutar el comando: {result.stderr}")

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise Exception(f"Error al decodificar JSON: {str(e)} - stdout: {result.stdout}")

# Función para calcular el puntaje basado en los resultados
def calcular_puntaje(resultados):
    total = len(resultados)
    correctos = resultados.count(True)
    return (correctos / total) * 100 if total > 0 else 0

@login_required
def ver_resultado(request, respuesta_id):
    respuesta = get_object_or_404(RespuestaEjercicio, id=respuesta_id)
    return render(request, 'ver_resultado.html', {'respuesta': respuesta})
from django.utils import timezone

@login_required
@user_passes_test(lambda u: not u.is_maestro)
def subir_respuesta(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)
    casos_de_prueba = ejercicio.casos_de_prueba
    respuesta = None  # Variable para almacenar la respuesta

    # Verificar si la fecha de entrega ha pasado
    if ejercicio.fecha_entrega < timezone.now():
        messages.error(request, f"La fecha de entrega ha pasado para el ejercicio {ejercicio.nombre_ejercicio}. No puedes subir respuestas.")
        return redirect('menu_alumno')

    if request.method == 'POST':
        form = RespuestaEjercicioForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.ejercicio = ejercicio
            respuesta.nombre_alumno = request.user.username

            if 'codigo_archivo' in request.FILES:
                archivo = request.FILES['codigo_archivo']
                archivo_path = os.path.join('/code/submissions', archivo.name)
                with open(archivo_path, 'wb+') as destination:
                    for chunk in archivo.chunks():
                        destination.write(chunk)
                respuesta.codigo_archivo = archivo_path

                # Copiar el archivo de código al contenedor executor
                os.system(f'docker cp {archivo_path} programacion-programacion-executor-1-1:/code/submissions/')

                # Crear y copiar el archivo de casos de prueba al contenedor executor
                casos_path = os.path.join('/code/submissions', 'casos_prueba.txt')
                with open(casos_path, 'w') as f:
                    f.write(casos_de_prueba)
                os.system(f'docker cp {casos_path} programacion-programacion-executor-1-1:/code/submissions/')

            try:
                with open(archivo_path, 'r') as file:
                    codigo = file.read()
                analizar_codigo(codigo)
            except Exception as e:
                messages.error(request, 'Archivo no permitido')
                return render(request, 'subir_respuesta.html', {'form': form, 'ejercicio': ejercicio, 'casos_de_prueba': casos_de_prueba})

            respuesta.save()

            if respuesta.codigo_archivo:
                code_path = f'/code/submissions/{archivo.name}'
                casos_path = '/code/submissions/casos_prueba.txt'
                task_id = add_task_to_queue(code_path, casos_path, respuesta.id)
                logger.info(f"Tarea {task_id} añadida a la cola.")
                messages.success(request, f'La respuesta se ha subido exitosamente y está en proceso de evaluación. Puntaje obtenido: {respuesta.puntaje}')

            return redirect('subir_respuesta', ejercicio_id=ejercicio.id)
    else:
        form = RespuestaEjercicioForm(user=request.user)

    # Obtener la última respuesta del usuario para este ejercicio
    ultima_respuesta = RespuestaEjercicio.objects.filter(ejercicio=ejercicio, nombre_alumno=request.user.username).last()
    
    return render(request, 'subir_respuesta.html', {'form': form, 'ejercicio': ejercicio, 'casos_de_prueba': casos_de_prueba, 'respuesta': ultima_respuesta})



@login_required
@user_passes_test(es_maestro)
def detalle_respuesta(request, respuesta_id):
    respuesta = get_object_or_404(RespuestaEjercicio, id=respuesta_id)
    if request.method == 'POST':
        respuesta.puntaje = request.POST.get('puntaje')
        respuesta.save()
        messages.success(request, 'El puntaje se ha guardado exitosamente.')
        return redirect('ver_respuestas', ejercicio_id=respuesta.ejercicio.id)
    return render(request, 'detalle_respuesta.html', {'respuesta': respuesta})

@login_required
@user_passes_test(es_maestro)
def ver_puntajes(request):
    respuestas = RespuestaEjercicio.objects.all()
    return render(request, 'ver_puntajes.html', {'respuestas': respuestas})

def custom_logout(request):
    auth_logout(request)
    request.session.flush()
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

from django.urls import reverse
@login_required
@user_passes_test(es_maestro)
def eliminar_ejercicio(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)
    ejercicio.delete()
    messages.success(request, 'El ejercicio se ha eliminado exitosamente.')
    return redirect(reverse('listar_ejercicios'))
