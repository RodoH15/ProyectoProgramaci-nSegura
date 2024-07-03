import os
from pathlib import Path
#from dotenv import load_dotenv
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Cargar variables de entorno desde el archivo .env
#load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_KEY')
DEBUG = 'True'
DATABASES = {
    'default': {
        #'ENGINE': os.getenv('DATABASE_ENGINE'),
        'ENGINE': "django.db.backends.mysql",
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        #'HOST': os.getenv('DATABASE_HOST'),
        'HOST': os.environ.get('DATABASE_HOST','programacion_bd_1'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}

ALLOWED_HOSTS = ['*', 'eminus5.uv', 'www.eminus5.uv']
CSRF_TRUSTED_ORIGINS = ['https://eminus5.uv', 'https://www.eminus5.uv']


TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
#ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'programacion',
    'django_extensions',
    'captcha',
]

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')


AUTH_USER_MODEL = 'programacion.Usuario'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'programacion.middleware.LoginAttemptMiddleware',
]

LOGIN_REDIRECT_URL = '/autenticacion/'
LOGIN_URL = '/login/'

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

MAX_UPLOAD_SIZE = 2 * 1024 * 1024  # 10 MB

WSGI_APPLICATION = 'programacion.wsgi.application'

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


#STATIC_ROOT = BASE_DIR / 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'sessionid'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = True  
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 900  # 15 minutos
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_AGE = 3600  # 1 hora


