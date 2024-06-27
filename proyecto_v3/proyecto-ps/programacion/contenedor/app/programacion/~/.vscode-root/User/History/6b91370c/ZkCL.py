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

from .scripts import inyect, evaluar, analizar_codigo  # Importar los scripts de evaluación


def index(request):
    return HttpResponse("<h1>Hola Mundo</h1>")

def password_valido(pass_a_evaluar: str, shadow: str) -> bool:
    _, algoritmo, salt, resumen = shadow.split('$')
    configuracion = '$%s$%s$' % (algoritmo, salt)
    shadow_nuevo = crypt.crypt(pass_a_evaluar, configuracion)
    return shadow_nuevo == shadow

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

            # Filtrar intentos recientes
            recent_attempts = FailedLoginAttempt.objects.filter(
                ip_address=ip_address,
                attempt_time__gt=now - lockout_time
            )

            # Bloquear si excede el límite de intentos
            if recent_attempts.count() >= attempt_limit:
                messages.error(request, f"Has alcanzado el límite de intentos. Intenta nuevamente en {lockout_time.seconds} segundos.")
                return render(request, 'login.html', {'form': form})

            try:
                user = Usuario.objects.get(username=username)
                if password_valido(password, user.password):
                    FailedLoginAttempt.objects.filter(ip_address=ip_address).delete()
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

def registro(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_exitoso')
    else:
        form = UsuarioForm()
    return render(request, 'registro.html', {'form': form})

def registro_exitoso(request):
    return render(request, 'registro_exitoso.html')

def generar_codigo_verificacion(length=8):
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(random.choice(caracteres) for i in range(length))
    return codigo

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
    return render(request, 'menu_alumno.html', {'ejercicios': ejercicios})

@login_required
@user_passes_test(es_maestro)
def menu_maestro(request):
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




import os
from .scripts import inyect, evaluar, analizar_codigo # Importar los scripts de evaluaciónss
from django.core.exceptions import ValidationError

# Validar el tipo de archivo
def validar_tipo_archivo(archivo):
    extensiones_permitidas = ['.py']
    extension = os.path.splitext(archivo.name)[1]
    if extension.lower() not in extensiones_permitidas:
        raise ValidationError('Tipo de archivo no permitido. Por favor, sube un archivo de Python (.py).')

# Validar el tamaño del archivo
def validar_tamano_archivo(archivo):
    tamano_maximo = 2 * 1024 * 1024  # 2 MB
    if archivo.size > tamano_maximo:
        raise ValidationError('El archivo es demasiado grande. El tamaño máximo permitido es 2 MB.')
    
from django.conf import settings

from django.contrib.messages import get_messages

from django.contrib import messages
from .scripts import evaluar, analizar_codigo

import subprocess
import json

@login_required
def subir_respuesta(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)
    casos_de_prueba = ejercicio.casos_de_prueba

    if request.method == 'POST':
        form = RespuestaEjercicioForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.ejercicio = ejercicio
            respuesta.nombre_alumno = request.user.username  # Asigna el nombre del alumno logueado automáticamente

            # Manejar la subida del archivo manualmente
            if 'codigo_archivo' in request.FILES:
                archivo = request.FILES['codigo_archivo']
                if archivo.size > settings.MAX_UPLOAD_SIZE:
                    messages.error(request, 'El archivo excede el límite de tamaño permitido de 10MB.')
                    return render(request, 'subir_respuesta.html', {'form': form, 'ejercicio': ejercicio, 'casos_de_prueba': casos_de_prueba})

                archivo_path = os.path.join('/code/submissions', archivo.name)  # Asegúrate de tener esta carpeta creada
                with open(archivo_path, 'wb+') as destination:
                    for chunk in archivo.chunks():
                        destination.write(chunk)
                respuesta.codigo_archivo = archivo_path

                # Copiar el archivo al contenedor executor
                os.system(f'docker cp {archivo_path} programacion_executor_1:/code/submissions/')

            try:
                with open(archivo_path, 'r') as file:
                    codigo = file.read()
                analizar_codigo(codigo)  # Analizar el código en busca de líneas peligrosas
            except Exception as e:
                messages.error(request, 'Archivo no permitido')
                return render(request, 'subir_respuesta.html', {'form': form, 'ejercicio': ejercicio, 'casos_de_prueba': casos_de_prueba})

            respuesta.save()

            # Evaluar el código subido
            if respuesta.codigo_archivo:
                code_path = f'/code/submissions/{archivo.name}'  # Ruta en el contenedor executor
                print(f"Evaluando el archivo de código en: {code_path}")
                print(f"Usando los casos de prueba: {casos_de_prueba}")

                # Pasar los casos de prueba directamente
                result = evaluar_con_casos_directos(code_path, casos_de_prueba)
                print(f"Resultado de la evaluación: {result}")
                respuesta.puntaje = calcular_puntaje(result)  # Función para calcular el puntaje basado en el resultado
                respuesta.save()
                print(f"Puntaje asignado: {respuesta.puntaje}")

            messages.success(request, f'La respuesta se ha subido exitosamente. Puntaje obtenido: {respuesta.puntaje}')
            return redirect('subir_respuesta', ejercicio_id=ejercicio.id)
    else:
        form = RespuestaEjercicioForm(user=request.user)
    return render(request, 'subir_respuesta.html', {'form': form, 'ejercicio': ejercicio, 'casos_de_prueba': casos_de_prueba})

def calcular_puntaje(result):
    total_cases = len(result)
    if total_cases == 0:
        return 0
    correct_cases = sum(1 for r in result if r is True)
    return (correct_cases / total_cases) * 100  # Porcentaje de casos correctos




def calcular_puntaje(result):
    """
    Función para calcular el puntaje basado en el resultado de la evaluación
    """
    total_cases = len(result)
    correct_cases = sum(1 for r in result if r is True)
    
    if total_cases == 0:
        return 0  # Evitar la división por cero

    return (correct_cases / total_cases) * 100  # Porcentaje de casos correctos

@login_required
@user_passes_test(es_maestro)
def ver_respuestas(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)
    respuestas = RespuestaEjercicio.objects.filter(ejercicio=ejercicio)
    return render(request, 'ver_respuestas.html', {'respuestas': respuestas, 'ejercicio': ejercicio})

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
