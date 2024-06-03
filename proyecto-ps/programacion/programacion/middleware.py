from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect
from django.contrib import messages
from .models import FailedLoginAttempt

class LoginAttemptMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'POST' and request.path == '/login/':  # Ajusta la ruta de tu vista de login
            ip_address = request.META.get('REMOTE_ADDR')
            now = timezone.now()
            attempt_limit = 3  # X cantidad de intentos inmediatos
            lockout_time = timedelta(seconds=60)  # Y cantidad de segundos de espera

            # Filtrar intentos recientes
            recent_attempts = FailedLoginAttempt.objects.filter(
                ip_address=ip_address,
                attempt_time__gt=now - lockout_time
            )

            # Bloquear si excede el límite de intentos
            if recent_attempts.count() >= attempt_limit:
                messages.error(request, f"Has alcanzado el límite de intentos. Intenta nuevamente en {lockout_time.seconds} segundos.")
                return redirect('login')  # Redirige a la página de login

    def process_response(self, request, response):
        if request.method == 'POST' and request.path == '/login/':
            if response.status_code == 200 and request.user.is_authenticated:
                ip_address = request.META.get('REMOTE_ADDR')
                # Eliminar los intentos fallidos después de un inicio de sesión exitoso
                FailedLoginAttempt.objects.filter(ip_address=ip_address).delete()
            elif response.status_code == 401:  # Ajusta según el código de respuesta de fallo de inicio de sesión
                ip_address = request.META.get('REMOTE_ADDR')
                # Registrar el intento fallido
                FailedLoginAttempt.objects.create(ip_address=ip_address)
        return response
