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


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
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

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
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
            return render(request, 'login.html')

        try:
            user = Usuario.objects.get(username=username)
            print(f"Usuario encontrado: {user.username}")
            if password_valido(password, user.password):
                print("Contraseña válida")
                FailedLoginAttempt.objects.filter(ip_address=ip_address).delete()
                auth_login(request, user)  # Inicia la sesión del usuario

                next_url = request.POST.get('next')
                if not next_url:
                    next_url = '/autenticacion/'

                print(f"Redirigiendo a {next_url}")
                print(f"Usuario autenticado: {request.user.is_authenticated}")
                return HttpResponseRedirect(next_url)
            else:
                print("Contraseña inválida")
                FailedLoginAttempt.objects.create(ip_address=ip_address)
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')
        except Usuario.DoesNotExist:
            print("Usuario no encontrado")
            FailedLoginAttempt.objects.create(ip_address=ip_address)
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')

    print("Renderizando la página de login")
    return render(request, 'login.html', {'next': request.GET.get('next', '')})

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

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ejercicio, RespuestaEjercicio

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

def custom_logout(request):
    auth_logout(request)
    request.session.flush()
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')
