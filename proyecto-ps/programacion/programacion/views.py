from django.http import HttpResponse  # Importa HttpResponse para devolver respuestas HTTP
from django.shortcuts import render, redirect, get_object_or_404  # Importa funciones de atajos de Django
from django.contrib import messages  # Importa el sistema de mensajes de Django
from django.utils import timezone  # Importa utilidades de tiempo de Django
from django.contrib.auth.decorators import login_required, user_passes_test  # Importa decoradores para la autenticación y permisos
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate  # Importa funciones de autenticación
from .telegram import enviar_mensaje  # Importa una función personalizada para enviar mensajes por Telegram
from .forms import CodigoAccesoForm, UsuarioForm, EjercicioForm, RespuestaEjercicioForm  # Importa formularios personalizados
from .models import Usuario, Ejercicio, FailedLoginAttempt, RespuestaEjercicio  # Importa modelos personalizados
import crypt  # Importa la librería crypt para manejar contraseñas
import string  # Importa la librería string para manejar cadenas de texto
import datetime  # Importa la librería datetime para manejar fechas y tiempos
import random  # Importa la librería random para generar valores aleatorios

# Vista para la página de inicio
def index(request):
    return HttpResponse("<h1>Hola Mundo</h1>")  # Devuelve una respuesta HTTP con un mensaje "Hola Mundo (esto fue solo de prueba)"

# Función para validar contraseñas
def password_valido(pass_a_evaluar: str, shadow: str) -> bool:
    _, algoritmo, salt, resumen = shadow.split('$')  # aqui divide el valor shadow en sus partes
    configuracion = '$%s$%s$' % (algoritmo, salt)  # Crea la funcion para la encriptacion
    shadow_nuevo = crypt.crypt(pass_a_evaluar, configuracion)  # Genera el hash de la contraseña a evaluar
    return shadow_nuevo == shadow  # Compara el hash generado con el hash almacenado

# Verifica si un usuario es maestro
def es_maestro(user):
    return user.is_maestro  # Devuelve True si el usuario es maestro

# Vista para el inicio de sesión
def login(request):
    if request.method == 'POST':  # Si el método de la solicitud es POST
        username = request.POST['username']  # Obtiene el nombre de usuario del formulario
        password = request.POST['password']  # Obtiene la contraseña del formulario
        ip_address = request.META.get('REMOTE_ADDR')  # Obtiene la dirección IP del cliente
        now = timezone.now()  # Obtiene la hora actual
        attempt_limit = 5  # Límite de intentos de inicio de sesión
        lockout_time = datetime.timedelta(seconds=60)  # Tiempo de bloqueo en segundos

        # Filtra los intentos recientes de inicio de sesión fallidos
        recent_attempts = FailedLoginAttempt.objects.filter(
            ip_address=ip_address,
            attempt_time__gt=now - lockout_time
        )

        if recent_attempts.count() >= attempt_limit:  # Si el número de intentos recientes supera el límite
            messages.error(request, f"Has alcanzado el límite de intentos. Intenta nuevamente en {lockout_time.seconds} segundos.")
            return render(request, 'login.html')  # devuelve la página de inicio de sesión con un mensaje de error

        try:
            user = Usuario.objects.get(username=username)  # intenta obtener el usuario por su nombre de usuario
            if password_valido(password, user.password):  # verifica si la contraseña es válida
                FailedLoginAttempt.objects.filter(ip_address=ip_address).delete()  # elimina los intentos fallidos para la ip (pruebas)
                request.session['username'] = username  #guarda el nombre de usuario en la sesión
                request.session['password'] = password  #guarda la contraseña en la sesión
                return redirect('autenticacion')  #redirige a la vista de autenticación
            else:
                FailedLoginAttempt.objects.create(ip_address=ip_address)  # crea un registro de intento fallido
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')  # muestra un mensaje de error
        except Usuario.DoesNotExist:  # Si el usuario no existe
            FailedLoginAttempt.objects.create(ip_address=ip_address)  # crea un registro de intento fallido
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')  # muestra un mensaje de error
    
    return render(request, 'login.html') 

# Vista para el registro de usuarios
def registro(request):
    if request.method == "POST":  # Si el método de la solicitud es POST
        form = UsuarioForm(request.POST)  # crea un formulario con los datos enviados
        if form.is_valid():  # si el formulario es válido
            form.save()  # guarda el nuevo usuario
            return redirect('registro_exitoso')  # redirige a la vista de registro exitoso (aun falta la pagina)
    else:
        form = UsuarioForm()  # crea un formulario vacío
    return render(request, 'registro.html', {'form': form})  # devuelve la página de registro con el formulario

# Vista para el mensaje de registro exitoso
def registro_exitoso(request):
    return render(request, 'registro_exitoso.html')  # devuelve la página de registro exitoso (aun falta la pagina)

# Genera un código de verificación aleatorio
def generar_codigo_verificacion(length=8):
    caracteres = string.ascii_letters + string.digits  # tipos de caracteres posibles
    codigo = ''.join(random.choice(caracteres) for i in range(length))  # genera el código aleatorio
    return codigo  # devuelve el código generado

# Vista para la autenticación de usuarios
def autenticacion(request):
    if request.method == 'POST':  # si el método de la solicitud es POST
        codigo_verificacion = generar_codigo_verificacion()  # genera un código de verificación
        mensaje = f'Su código de verificación es: {codigo_verificacion}'  # crea el mensaje con el código

        if enviar_mensaje(mensaje):  # funcion para ennvía el mensaje y verifica si fue exitoso
            request.session['codigo_correcto'] = codigo_verificacion  # guarda el código en la sesión
            request.session['codigo_generado'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # guarda la hora de generación del código
            return redirect('ingresar_codigo_acceso')  # redirecciona a la vista para ingresar el código de acceso
        else:
            return HttpResponse('Hubo un error al enviar el código de verificación.')  # devuelve un mensaje de error si el envío falla
    return render(request, 'autenticacion.html')  # devuelve la página de autenticación

# Vista para ingresar el código de acceso
def ingresar_codigo_acceso(request):
    if request.method == 'POST':  # si el método de la solicitud es POST
        form = CodigoAccesoForm(request.POST)  # crea un formulario con los datos enviados
        if form.is_valid():  # si el formulario es válido
            codigo_ingresado = form.cleaned_data['codigo_acceso']  # obtiene el código ingresado
            codigo_correcto = request.session.get('codigo_correcto')  # obtiene el código correcto de la sesión
            codigo_generado = request.session.get('codigo_generado')  # obtiene la hora de generación del código

            if not codigo_correcto or not codigo_generado:  # si no hay un código correcto o una hora de generación
                return HttpResponse("Intento de reutilización del código detectado. Por favor, solicita un nuevo código.")  # devuelve un mensaje de error
                
            if codigo_correcto and codigo_generado:  # si hay un código correcto y una hora de generación
                codigo_generado_dt = datetime.datetime.strptime(codigo_generado, '%Y-%m-%d %H:%M:%S')  # aqui convierte la hora de generación a datetime
                tiempo_transcurrido = datetime.datetime.now() - codigo_generado_dt  # calcula el tiempo transcurrido
                tiempo_maximo = datetime.timedelta(minutes=3)  # tiempo máximo permitido

                if tiempo_transcurrido > tiempo_maximo:  # si el tiempo transcurrido supera el tiempo máximo
                    return HttpResponse("El código ha expirado. Por favor, solicita un nuevo código.")  # Devuelve un mensaje de error
                elif codigo_ingresado == codigo_correcto:  # si el código ingresado es correcto
                    username = request.session.get('username')  # Obtiene el nombre de usuario de la sesión
                    password = request.session.get('password')  # Obtiene la contraseña de la sesión

                    # Autenticación manual
                    try:
                        user = Usuario.objects.get(username=username)  # obtiene el usuario por su nombre de usuario
                        if password_valido(password, user.password):  # verifica si la contraseña es válida
                            auth_login(request, user)  # snicia sesión manualmente
                            if user.is_maestro:  #si el usuario es maestro
                                return redirect('menu_maestro')  # redirige al menú de maestro
                            else:
                                return redirect('menu_alumno')  # redirige al menú de alumno
                        else:
                            return HttpResponse("Error de autenticación. Contraseña incorrecta.")  # devuelve un mensaje de error si la contraseña es incorrecta
                    except Usuario.DoesNotExist:  # Si el usuario no existe
                        return HttpResponse("Error de autenticación. Usuario no existe.")  # evuelve un mensaje de error si el usuario no existe
                else:
                    return HttpResponse("Código de acceso incorrecto. Por favor, inténtalo de nuevo.")  # devuelve un mensaje de error si el código es incorrecto
    else:
        form = CodigoAccesoForm()  # Crea un formulario vacío

    return render(request, 'ingresar_codigo_acceso.html', {'form': form})  # Devuelve la página para ingresar el código de acceso con el formulario

# Vista para ver respuestas de ejercicios (requiere inicio de sesión)
@login_required
def ver_respuestas(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)  # obtiene el ejercicio o devuelve 404 si no existe
    respuestas = RespuestaEjercicio.objects.filter(ejercicio=ejercicio)  # filtra las respuestas del ejercicio
    return render(request, 'ver_respuestas.html', {'respuestas': respuestas, 'ejercicio': ejercicio})  # devuelve la página con las respuestas del ejercicio

# vista para el menú de maestros (requiere inicio de sesión)
@login_required
def menu_maestro(request):
    ejercicios = Ejercicio.objects.all()  # obtiene todos los ejercicios
    respuestas = RespuestaEjercicio.objects.all()  # obtiene todas las respuestas
    return render(request, 'menu_maestro.html', {'ejercicios': ejercicios, 'respuestas': respuestas})  # Devuelve la página del menú de maestros con los ejercicios y respuestas

# Vista para el menú de alumnos (requiere inicio de sesión)
@login_required
def menu_alumno(request):
    ejercicios = Ejercicio.objects.all()  # obtiene todos los ejercicios
    return render(request, 'menu_alumno.html', {'ejercicios': ejercicios})  # devuelve la página del menú de alumnos con los ejercicios

# Vista para cerrar sesión
def logout_view(request):
    auth_logout(request)  # cierra la sesión del usuario
    return redirect('login')  # redirige a la página de inicio de sesión

# Vista para crear ejercicios (requiere inicio de sesión y ser maestro)
@login_required
@user_passes_test(es_maestro)
def crear_ejercicio(request):
    if request.method == 'POST':  # Si el método de la solicitud es POST
        form = EjercicioForm(request.POST)  # Crea un formulario con los datos enviados
        if form.is_valid():  # Si el formulario es válido
            form.save()  # Guarda el nuevo ejercicio
            messages.success(request, 'El ejercicio se ha creado exitosamente.')  # muestra un mensaje de éxito
            return redirect('listar_ejercicios')  # redirige a la lista de ejercicios
    else:
        form = EjercicioForm() 
    return render(request, 'crear_ejercicio.html', {'form': form})  # devuelve la página para crear ejercicios con el formulario

# Vista para listar ejercicios (requiere inicio de sesión)
@login_required
def listar_ejercicios(request):
    ejercicios = Ejercicio.objects.all()  # Obtiene todos los ejercicios
    return render(request, 'listar_ejercicios.html', {'ejercicios': ejercicios})  # Devuelve la página con la lista de ejercicios

# Vista para ver el detalle de un ejercicio (requiere inicio de sesión)
@login_required
def detalle_ejercicio(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)  # Obtiene el ejercicio o devuelve 404 si no existe
    return render(request, 'detalle_ejercicio.html', {'ejercicio': ejercicio})  # Devuelve la página con el detalle del ejercicio

# Vista para subir respuestas de ejercicios (requiere inicio de sesión)
@login_required
def subir_respuesta(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)  # Obtiene el ejercicio o devuelve 404 si no existe
    if request.method == 'POST':  # Si el método de la solicitud es POST
        form = RespuestaEjercicioForm(request.POST)  # Crea un formulario con los datos enviados
        if form.is_valid():  # Si el formulario es válido
            respuesta = form.save(commit=False)  # Guarda la respuesta sin confirmar
            respuesta.ejercicio = ejercicio  # Asigna el ejercicio a la respuesta
            respuesta.save()  # Guarda la respuesta
            messages.success(request, 'La respuesta se ha subido exitosamente.')  # Muestra un mensaje de éxito
            return redirect('ver_respuestas', ejercicio_id=ejercicio.id)  # Redirige a la vista de respuestas del ejercicio
    else:
        form = RespuestaEjercicioForm()  # Crea un formulario vacío
    return render(request, 'subir_respuesta.html', {'form': form, 'ejercicio': ejercicio})  # Devuelve la página para subir respuestas con el formulario y el ejercicio

# Vista para ver respuestas de ejercicios (requiere inicio de sesión y ser maestro)
@login_required
@user_passes_test(es_maestro)
def ver_respuestas(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)  # Obtiene el ejercicio o devuelve 404 si no existe
    respuestas = RespuestaEjercicio.objects.filter(ejercicio=ejercicio)  # Filtra las respuestas del ejercicio
    return render(request, 'ver_respuestas.html', {'respuestas': respuestas, 'ejercicio': ejercicio})  # Devuelve la página con las respuestas del ejercicio

# Vista para ver el detalle de una respuesta (requiere inicio de sesión y ser maestro)
@login_required
@user_passes_test(es_maestro)
def detalle_respuesta(request, respuesta_id):
    respuesta = get_object_or_404(RespuestaEjercicio, id=respuesta_id)  # Obtiene la respuesta o devuelve 404 si no existe
    if request.method == 'POST':  # Si el método de la solicitud es POST
        respuesta.puntaje = request.POST.get('puntaje')  # Obtiene el puntaje del formulario
        respuesta.save()  # Guarda la respuesta
        messages.success(request, 'El puntaje se ha guardado exitosamente.')  # Muestra un mensaje de éxito
        return redirect('ver_respuestas', ejercicio_id=respuesta.ejercicio.id)  # Redirige a la vista de respuestas del ejercicio
    return render(request, 'detalle_respuesta.html', {'respuesta': respuesta})  # Devuelve la página con el detalle de la respuesta

# Vista para ver puntajes (requiere inicio de sesión y ser maestro)
@login_required
@user_passes_test(es_maestro)
def ver_puntajes(request):
    respuestas = RespuestaEjercicio.objects.all()  # Obtiene todas las respuestas
    return render(request, 'ver_puntajes.html', {'respuestas': respuestas})  # Devuelve la página con los puntajes de las respuestas

# Vista personalizada para cerrar sesión
from django.contrib.auth import logout  # Importa la función de logout
from django.shortcuts import redirect  # Importa la función de redirección
from django.contrib import messages  # Importa el sistema de mensajes

def custom_logout(request):
    logout(request)  # Cierra la sesión del usuario
    request.session.flush()  # Limpia la sesión
    messages.success(request, 'Has cerrado sesión exitosamente.')  # Muestra un mensaje de éxito
    return redirect('login')  # Redirige a la página de inicio de sesión
