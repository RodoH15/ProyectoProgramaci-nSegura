from django import forms
from .models import Usuario
import re
import crypt
import base64
import os
from .models import Ejercicio, RespuestaEjercicio
from django import forms
from captcha.fields import CaptchaField

#from django import forms
from .models import Ejercicio, RespuestaEjercicio, Usuario
# Formulario para ingresar el código de acceso
class CodigoAccesoForm(forms.Form):
    codigo_acceso = forms.CharField(label='Código de acceso', max_length=8, widget=forms.TextInput(attrs={'class': 'form-control'}))

    """
# Formulario para registrar un nuevo usuario
class UsuarioForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Usuario  # Modelo que se asocia al formulario
        fields = ['username', 'email', 'password']  # Campos del modelo que se incluirán en el formulario
        widgets = {
            'password': forms.PasswordInput(),  # Se confirma la contraseña
        }
            """
    

class UsuarioForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    bot_id = forms.CharField(max_length=100, required=True, help_text='Bot ID de Telegram')  # Nuevo campo para bot_id
    chat_id = forms.CharField(max_length=100, required=True, help_text='Chat ID de Telegram')  # Nuevo campo para chat_id

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'bot_id', 'chat_id']  # Incluye los nuevos campos
        widgets = {
            'password': forms.PasswordInput(),
        }

    # Función para definir las políticas de contraseñas
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 10:
            raise forms.ValidationError("La contraseña debe tener al menos 10 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("La contraseña debe contener al menos una letra minúscula.")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un dígito.")
        if not re.search(r'[@$!%*?&]', password):
            raise forms.ValidationError("La contraseña debe contener al menos un carácter especial.")
        return password

    # Validar que las contraseñas coincidan y realizar el hashing de las contraseñas antes de guardar
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        # Hashear la contraseña
        salt = generar_salt()  # Genera un salt aleatorio
        hashed_password = crypt.crypt(password, f'$6${salt}')  # Hashea la contraseña usando SHA-512
        cleaned_data['password'] = hashed_password  # Reemplaza la contraseña con la versión hasheada
        return cleaned_data

# Generar un salt aleatorio para usar en el hashing de contraseñas
def generar_salt(tamano=16):
    aleatorio = os.urandom(tamano)  # Genera una cadena de bytes aleatorios
    return base64.b64encode(aleatorio).decode('utf-8')  # Codifica la cadena en base64

# forms.py

from django import forms
from .models import Ejercicio

class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre_ejercicio', 'descripcion_ejercicio', 'fecha_inicio', 'fecha_entrega', 'casos_de_prueba']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'class': 'datetimepicker'}),
            'fecha_entrega': forms.DateTimeInput(attrs={'class': 'datetimepicker'}),
        }

        

from django import forms
from .models import RespuestaEjercicio

class RespuestaEjercicioForm(forms.ModelForm):
    class Meta:
        model = RespuestaEjercicio
        fields = ['nombre_alumno', 'respuesta', 'codigo_archivo']
        widgets = {
            'nombre_alumno': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    codigo_archivo = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RespuestaEjercicioForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['nombre_alumno'].initial = user.username


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    captcha = CaptchaField()  # Añadir el campo Captcha
