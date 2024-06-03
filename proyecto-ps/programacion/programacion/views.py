from django.http import HttpResponse # importa la clase HttpResponse del módulo django.http
from django.shortcuts import render, redirect, get_object_or_404 # importa las funciones render, redirect y get_object_or_404 del módulo django.shortcuts
from django.contrib import messages # importa el módulo messages de django.contrib
from django.utils import timezone # importa el módulo timezone de django.utils
from django.contrib.auth.decorators import login_required, user_passes_test # importa los decoradores login_required y user_passes_test de django.contrib.auth.decorators
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate # importa las funciones login, logout y authenticate de django.contrib.auth
from .telegram import enviar_mensaje # importa la función enviar_mensaje del módulo .telegram
from .forms import CodigoAccesoForm, UsuarioForm, EjercicioForm, RespuestaEjercicioForm # importa los formularios del módulo .forms
from .models import Usuario, Ejercicio, FailedLoginAttempt, RespuestaEjercicio # importa los modelos del módulo .models
import crypt # importa el módulo crypt
import string # importa el módulo string
import datetime # importa el módulo datetime
import random # importa el módulo random

def index(request): # define la vista index
    return HttpResponse("<h1>Hola Mundo</h1>") # retorna una respuesta HTTP con el mensaje "Hola Mundo"

def password_valido(pass_a_evaluar: str, shadow: str) -> bool: # define la función password_valido
    _, algoritmo, salt, resumen = shadow.split('$') # separa el hash shadow en partes
    configuracion = '$%s$%s$' % (algoritmo, salt) # crea la configuración del hash
    shadow_nuevo = crypt.crypt(pass_a_evaluar, configuracion) # genera el hash para la contraseña a evaluar
    return shadow_nuevo == shadow # retorna True si los hashes coinciden, False en caso contrario

def es_maestro(user): # define la función es_maestro
    return user.is_maestro # retorna si el usuario es maestro

def login(request): # define la vista login
    if request.method == 'POST': # verifica si el método de la solicitud es POST
        username = request.POST['username'] # obtiene el nombre de usuario del formulario
        password = request.POST['password'] # obtiene la contraseña del formulario
        ip_address = request.META.get('REMOTE_ADDR') # obtiene la dirección IP del cliente
        now = timezone.now() # obtiene la fecha y hora actual
        attempt_limit = 5 # establece el límite de intentos fallidos
        lockout_time = datetime.timedelta(seconds=60) # establece el tiempo de bloqueo

        recent_attempts = FailedLoginAttempt.objects.filter( # filtra los intentos fallidos recientes
            ip_address=ip_address,
            attempt_time__gt=now - lockout_time
        )

        if recent_attempts.count() >= attempt_limit: # verifica si se ha alcanzado el límite de intentos
            messages.error(request, f"Has alcanzado el límite de intentos. Intenta nuevamente en {lockout_time.seconds} segundos.") # muestra un mensaje de error
            return render(request, 'login.html') # renderiza la plantilla login.html

        try:
            user = Usuario.objects.get(username=username) # busca el usuario en la base de datos
            if password_valido(password, user.password): # verifica si la contraseña es válida
                FailedLoginAttempt.objects.filter(ip_address=ip_address).delete() # elimina los intentos fallidos
                request.session['username'] = username # guarda el nombre de usuario en la sesión
                request.session['password'] = password # guarda la contraseña en la sesión
                return redirect('autenticacion') # redirige a la vista autenticacion
            else:
                FailedLoginAttempt.objects.create(ip_address=ip_address) # crea un intento fallido
                messages.error(request, 'Nombre de usuario o contraseña incorrectos') # muestra un mensaje de error
        except Usuario.DoesNotExist: # maneja la excepción si el usuario no existe
            FailedLoginAttempt.objects.create(ip_address=ip_address) # crea un intento fallido
            messages.error(request, 'Nombre de usuario o contraseña incorrectos') # muestra un mensaje de error

    return render(request, 'login.html') # renderiza la plantilla login.html

def registro(request): # define la vista registro
    if request.method == "POST": # verifica si el método de la solicitud es POST
        form = UsuarioForm(request.POST) # crea una instancia del formulario UsuarioForm con los datos del formulario
        if form.is_valid(): # verifica si el formulario es válido
            form.save() # guarda el nuevo usuario
            return redirect('registro_exitoso') # redirige a la vista registro_exitoso
    else:
        form = UsuarioForm() # crea una instancia vacía del formulario UsuarioForm
    return render(request, 'registro.html', {'form': form}) # renderiza la plantilla registro.html con el formulario

def registro_exitoso(request): # define la vista registro_exitoso
    return render(request, 'registro_exitoso.html') # renderiza la plantilla registro_exitoso.html

def generar_codigo_verificacion(length=8): # define la función generar_codigo_verificacion
    caracteres = string.ascii_letters + string.digits # define los caracteres permitidos
    codigo = ''.join(random.choice(caracteres) for i in range(length)) # genera un código aleatorio
    return codigo # retorna el código generado

def autenticacion(request): # define la vista autenticacion
    if request.method == 'POST': # verifica si el método de la solicitud es POST
        codigo_verificacion = generar_codigo_verificacion() # genera un código de verificación
        mensaje = f'Su código de verificación es: {codigo_verificacion}' # crea el mensaje con el código

        if enviar_mensaje(mensaje): # verifica si el mensaje se envió correctamente
            request.session['codigo_correcto'] = codigo_verificacion # guarda el código en la sesión
            request.session['codigo_generado'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # guarda la fecha y hora de generación del código
            return redirect('ingresar_codigo_acceso') # redirige a la vista ingresar_codigo_acceso
        else:
            return HttpResponse('Hubo un error al enviar el código de verificación.') # retorna un mensaje de error
    return render(request, 'autenticacion.html') # renderiza la plantilla autenticacion.html

def ingresar_codigo_acceso(request): # define la vista ingresar_codigo_acceso
    if request.method == 'POST': # verifica si el método de la solicitud es POST
        form = CodigoAccesoForm(request.POST) # crea una instancia del formulario CodigoAccesoForm con los datos del formulario
        if form.is_valid(): # verifica si el formulario es válido
            codigo_ingresado = form.cleaned_data['codigo_acceso'] # obtiene el código ingresado del formulario
            codigo_correcto = request.session.get('codigo_correcto') # obtiene el código correcto de la sesión
            codigo_generado = request.session.get('codigo_generado') # obtiene la fecha y hora de generación del código de la sesión

            if not codigo_correcto or not codigo_generado: # verifica si falta el código o la fecha de generación en la sesión
                messages.error(request, "Intento de reutilización del código detectado. Por favor, solicita un nuevo código.") # muestra un mensaje de error
                return redirect('login') # redirige a la vista login

            if codigo_correcto and codigo_generado: # verifica si el código y la fecha de generación están presentes
                codigo_generado_dt = datetime.datetime.strptime(codigo_generado, '%Y-%m-%d %H:%M:%S') # convierte la fecha de generación a un objeto datetime
                tiempo_transcurrido = datetime.datetime.now() - codigo_generado_dt # calcula el tiempo transcurrido desde la generación del código
                tiempo_maximo = datetime.timedelta(minutes=3) # establece el tiempo máximo de vida del código

                if tiempo_transcurrido > tiempo_maximo: # verifica si el código ha expirado
                    messages.error(request, "El código ha expirado. Por favor, solicita un nuevo código.") # muestra un mensaje de error
                    return redirect('login') # redirige a la vista login
                elif codigo_ingresado == codigo_correcto: # verifica si el código ingresado es correcto
                    username = request.session.get('username') # obtiene el nombre de usuario de la sesión
                    password = request.session.get('password') # obtiene la contraseña de la sesión

                    try:
                        user = Usuario.objects.get(username=username) # busca el usuario en la base de datos
                        if password_valido(password, user.password): # verifica si la contraseña es válida
                            auth_login(request, user) # inicia sesión
                            if user.is_maestro: # verifica si el usuario es maestro
                                return redirect('menu_maestro') # redirige a la vista menu_maestro
                            else:
                                return redirect('menu_alumno') # redirige a la vista menu_alumno
                        else:
                            messages.error(request, "Error de autenticación. Contraseña incorrecta.") # muestra un mensaje de error
                            return redirect('login') # redirige a la vista login
                    except Usuario.DoesNotExist: # maneja la excepción si el usuario no existe
                        messages.error(request, "Error de autenticación. Usuario no existe.") # muestra un mensaje de error
                        return redirect('login') # redirige a la vista login
                else:
                    messages.error(request, "Código de acceso incorrecto. Por favor, inténtalo de nuevo.") # muestra un mensaje de error
                    return redirect('login') # redirige a la vista login
    else:
        form = CodigoAccesoForm() # crea una instancia vacía del formulario CodigoAccesoForm

    return render(request, 'ingresar_codigo_acceso.html', {'form': form}) # renderiza la plantilla ingresar_codigo_acceso.html con el formulario

@login_required # asegura que el usuario esté autenticado
def ver_respuestas(request, ejercicio_id): # define la vista ver_respuestas
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id) # obtiene el ejercicio o retorna 404 si no existe
    respuestas = RespuestaEjercicio.objects.filter(ejercicio=ejercicio) # obtiene las respuestas del ejercicio
    return render(request, 'ver_respuestas.html', {'respuestas': respuestas, 'ejercicio': ejercicio}) # renderiza la plantilla ver_respuestas.html con las respuestas y el ejercicio

@login_required # asegura que el usuario esté autenticado
def menu_maestro(request): # define la vista menu_maestro
    ejercicios = Ejercicio.objects.all() # obtiene todos los ejercicios
    respuestas = RespuestaEjercicio.objects.all() # obtiene todas las respuestas
    return render(request, 'menu_maestro.html', {'ejercicios': ejercicios, 'respuestas': respuestas}) # renderiza la plantilla menu_maestro.html con los ejercicios y las respuestas

@login_required # asegura que el usuario esté autenticado
def menu_alumno(request): # define la vista menu_alumno
    ejercicios = Ejercicio.objects.all() # obtiene todos los ejercicios
    return render(request, 'menu_alumno.html', {'ejercicios': ejercicios}) # renderiza la plantilla menu_alumno.html con los ejercicios

def logout_view(request): # define la vista logout_view
    auth_logout(request) # cierra la sesión del usuario
    return redirect('login') # redirige a la vista login

@login_required # asegura que el usuario esté autenticado
@user_passes_test(es_maestro) # asegura que el usuario sea maestro
def crear_ejercicio(request): # define la vista crear_ejercicio
    if request.method == 'POST': # verifica si el método de la solicitud es POST
        form = EjercicioForm(request.POST) # crea una instancia del formulario EjercicioForm con los datos del formulario
        if form.is_valid(): # verifica si el formulario es válido
            form.save() # guarda el nuevo ejercicio
            messages.success(request, 'El ejercicio se ha creado exitosamente.') # muestra un mensaje de éxito
            return redirect('listar_ejercicios') # redirige a la vista listar_ejercicios
    else:
        form = EjercicioForm() # crea una instancia vacía del formulario EjercicioForm
    return render(request, 'crear_ejercicio.html', {'form': form}) # renderiza la plantilla crear_ejercicio.html con el formulario

@login_required # asegura que el usuario esté autenticado
def listar_ejercicios(request): # define la vista listar_ejercicios
    ejercicios = Ejercicio.objects.all() # obtiene todos los ejercicios
    return render(request, 'listar_ejercicios.html', {'ejercicios': ejercicios}) # renderiza la plantilla listar_ejercicios.html con los ejercicios

@login_required # asegura que el usuario esté autenticado
def detalle_ejercicio(request, ejercicio_id): # define la vista detalle_ejercicio
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id) # obtiene el ejercicio o retorna 404 si no existe
    return render(request, 'detalle_ejercicio.html', {'ejercicio': ejercicio}) # renderiza la plantilla detalle_ejercicio.html con el ejercicio

@login_required # asegura que el usuario esté autenticado
def subir_respuesta(request, ejercicio_id): # define la vista subir_respuesta
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id) # obtiene el ejercicio o retorna 404 si no existe
    if request.method == 'POST': # verifica si el método de la solicitud es POST
        form = RespuestaEjercicioForm(request.POST) # crea una instancia del formulario RespuestaEjercicioForm con los datos del formulario
        if form.is_valid(): # verifica si el formulario es válido
            respuesta = form.save(commit=False) # guarda la respuesta sin cometer
            respuesta.ejercicio = ejercicio # asigna el ejercicio a la respuesta
            respuesta.save() # guarda la respuesta
            messages.success(request, 'La respuesta se ha subido exitosamente.') # muestra un mensaje de éxito
            return redirect('ver_respuestas', ejercicio_id=ejercicio.id) # redirige a la vista ver_respuestas
    else:
        form = RespuestaEjercicioForm() # crea una instancia vacía del formulario RespuestaEjercicioForm
    return render(request, 'subir_respuesta.html', {'form': form, 'ejercicio': ejercicio}) # renderiza la plantilla subir_respuesta.html con el formulario y el ejercicio

@login_required # asegura que el usuario esté autenticado
@user_passes_test(es_maestro) # asegura que el usuario sea maestro
def ver_respuestas(request, ejercicio_id): # define la vista ver_respuestas
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id) # obtiene el ejercicio o retorna 404 si no existe
    respuestas = RespuestaEjercicio.objects.filter(ejercicio=ejercicio) # obtiene las respuestas del ejercicio
    return render(request, 'ver_respuestas.html', {'respuestas': respuestas, 'ejercicio': ejercicio}) # renderiza la plantilla ver_respuestas.html con las respuestas y el ejercicio

@login_required # asegura que el usuario esté autenticado
@user_passes_test(es_maestro) # asegura que el usuario sea maestro
def detalle_respuesta(request, respuesta_id): # define la vista detalle_respuesta
    respuesta = get_object_or_404(RespuestaEjercicio, id=respuesta_id) # obtiene la respuesta o retorna 404 si no existe
    if request.method == 'POST': # verifica si el método de la solicitud es POST
        respuesta.puntaje = request.POST.get('puntaje') # asigna el puntaje a la respuesta
        respuesta.save() # guarda la respuesta
        messages.success(request, 'El puntaje se ha guardado exitosamente.') # muestra un mensaje de éxito
        return redirect('ver_respuestas', ejercicio_id=respuesta.ejercicio.id) # redirige a la vista ver_respuestas
    return render(request, 'detalle_respuesta.html', {'respuesta': respuesta}) # renderiza la plantilla detalle_respuesta.html con la respuesta

@login_required # asegura que el usuario esté autenticado
@user_passes_test(es_maestro) # asegura que el usuario sea maestro
def ver_puntajes(request): # define la vista ver_puntajes
    respuestas = RespuestaEjercicio.objects.all() # obtiene todas las respuestas
    return render(request, 'ver_puntajes.html', {'respuestas': respuestas}) # renderiza la plantilla ver_puntajes.html con las respuestas

from django.contrib.auth import logout # importa la función logout de django.contrib.auth
from django.shortcuts import redirect # importa la función redirect de django.shortcuts
from django.contrib import messages # importa el módulo messages de django.contrib

def custom_logout(request): # define la vista custom_logout
    logout(request) # cierra la sesión del usuario
    request.session.flush() # limpia la sesión
    messages.success(request, 'Has cerrado sesión exitosamente.') # muestra un mensaje de éxito
    return redirect('login') # redirige a la vista login
