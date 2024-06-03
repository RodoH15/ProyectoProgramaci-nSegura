import os
from pathlib import Path

# Define BASE_DIR antes de usarlo
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración directamente en settings.py
SECRET_KEY = 'django-insecure-(23+^tx!(u9*%ku+cv%w_a2qf#vzrs+o8dtr+*6ofkx6wv)g+k'
DEBUG = True
DATABASE_URL = 'sqlite:///db.sqlite3'
TOKEN = '7344186903:AAGRtOSxvTq0zDcG5slbsjF3xfFsNNaiReY'
CHAT_ID = '1436880940'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'programacion',
    'django_extensions',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'programacion.middleware.LoginAttemptMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'programacion.middleware.LoginAttemptMiddleware',
]

LOGIN_REDIRECT_URL = 'autenticacion'

ROOT_URLCONF = 'programacion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'programacion.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ps',
        'USER': 'tux',
        'PASSWORD': 'V1c+0rm4n0',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Asegúrate de que se actualice la sesión con cada solicitud
SESSION_SAVE_EVERY_REQUEST = True
# Establece que la sesión expire al cerrar el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = True  
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_AGE = 900  # 1 hora
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'menu_alumno' 
AUTH_USER_MODEL = 'programacion.Usuario'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'  # Puede ser 'Lax', 'Strict' o 'None'
CSRF_COOKIE_SAMESITE = 'Strict'
# Configurar la cookie de sesión para que sólo se envíe a través de HTTPS
#SESSION_COOKIE_SECURE = True

# Configurar la cookie CSRF para que sólo se envíe a través de HTTPS
#CSRF_COOKIE_SECURE = True

# Hacer que las cookies expiren al cerrar la pestaña del navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Configurar la edad de la cookie de sesión en segundos (por ejemplo, 1 hora)
SESSION_COOKIE_AGE = 3600  # 1 hora

# Configurar la edad de la cookie CSRF en segundos (opcional)
CSRF_COOKIE_AGE = 3600  # 1 hora