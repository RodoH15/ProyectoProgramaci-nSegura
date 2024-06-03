from django.http import HttpResponse
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

def index(request):
    return HttpResponse("<h1>Hola Mundo</h1>")

def password_valido(pass_a_evaluar: str, shadow: str) -> bool:
    _, algoritmo, salt, resumen = shadow.split('$')
    configuracion = '$%s$%s$' % (algoritmo, salt)
    shadow_nuevo = crypt.crypt(pass_a_evaluar, configuracion)
    return shadow_nuevo == shadow

def es_maestro(user):
    return user.is_maestro

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
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
            return render(request, 'login.html')

        try:
            user = Usuario.objects.get(username=username)
            if password_valido(password, user.password):
                FailedLoginAttempt.objects.filter(ip_address=ip_address).delete()
                request.session['username'] = username
                request.session['password'] = password
                return redirect('autenticacion')
            else:
                FailedLoginAttempt.objects.create(ip_address=ip_address)
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')
        except Usuario.DoesNotExist:
            FailedLoginAttempt.objects.create(ip_address=ip_address)
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

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

def ingresar_codigo_acceso(request):
    if request.method == 'POST':
        form = CodigoAccesoForm(request.POST)
        if form.is_valid():
            codigo_ingresado = form.cleaned_data['codigo_acceso']
            codigo_correcto = request.session.get('codigo_correcto')
            codigo_generado = request.session.get('codigo_generado')

            print(f"codigo_ingresado: {codigo_ingresado}, codigo_correcto: {codigo_correcto}")

            if not codigo_correcto or not codigo_generado:
                print("Intento de reutilización del código detectado.")
                return HttpResponse("Intento de reutilización del código detectado. Por favor, solicita un nuevo código.")

            if codigo_correcto and codigo_generado:
                codigo_generado_dt = datetime.datetime.strptime(codigo_generado, '%Y-%m-%d %H:%M:%S')
                tiempo_transcurrido = datetime.datetime.now() - codigo_generado_dt
                tiempo_maximo = datetime.timedelta(minutes=3)

                if tiempo_transcurrido > tiempo_maximo:
                    print("El código ha expirado.")
                    return HttpResponse("El código ha expirado. Por favor, solicita un nuevo código.")
                elif codigo_ingresado == codigo_correcto:
                    username = request.session.get('username')
                    password = request.session.get('password')
                    print(f"Autenticando usuario: {username} con contraseña: {password}")

                    # Autenticación manual
                    try:
                        user = Usuario.objects.get(username=username)
                        if password_valido(password, user.password):
                            print("Autenticación manual exitosa")
                            auth_login(request, user)
                            if user.is_maestro:
                                return redirect('menu_maestro')
                            else:
                                return redirect('menu_alumno')
                        else:
                            print("Falló la autenticación manual: contraseña incorrecta")
                            return HttpResponse("Error de autenticación. Contraseña incorrecta.")
                    except Usuario.DoesNotExist:
                        print("Falló la autenticación manual: usuario no existe")
                        return HttpResponse("Error de autenticación. Usuario no existe.")
                else:
                    print("Código de acceso incorrecto")
                    return HttpResponse("Código de acceso incorrecto. Por favor, inténtalo de nuevo.")
    else:
        form = CodigoAccesoForm()

    return render(request, 'ingresar_codigo_acceso.html', {'form': form})


@login_required
def ver_respuestas(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)
    respuestas = RespuestaEjercicio.objects.filter(ejercicio=ejercicio)
    return render(request, 'ver_respuestas.html', {'respuestas': respuestas, 'ejercicio': ejercicio})

@login_required
@login_required
def menu_maestro(request):
    ejercicios = Ejercicio.objects.all()
    respuestas = RespuestaEjercicio.objects.all()  # Asumiendo que tienes una clase RespuestaEjercicio
    return render(request, 'menu_maestro.html', {'ejercicios': ejercicios, 'respuestas': respuestas})

@login_required
def menu_alumno(request):
    ejercicios = Ejercicio.objects.all()
    return render(request, 'menu_alumno.html', {'ejercicios': ejercicios})

@login_required
def menu_alumno(request):
    return render(request, 'menu_alumno.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
@user_passes_test(es_maestro)
def crear_ejercicio(request):
    if request.method == 'POST':
        form = EjercicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El ejercicio se ha creado exitosamente.')
            return redirect('listar_ejercicios')
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
    return render(request, 'detalle_ejercicio.html', {'ejercicio': ejercicio})

@login_required
def subir_respuesta(request, ejercicio_id):
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)
    if request.method == 'POST':
        form = RespuestaEjercicioForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.ejercicio = ejercicio
            respuesta.save()
            messages.success(request, 'La respuesta se ha subido exitosamente.')
            return redirect('ver_respuestas', ejercicio_id=ejercicio.id)
    else:
        form = RespuestaEjercicioForm()
    return render(request, 'subir_respuesta.html', {'form': form, 'ejercicio': ejercicio})

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



from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def custom_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')  # Redirige al usuario a la página de inicio de sesión después de cerrar la sesión
