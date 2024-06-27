from django.urls import path, include
from .views import login, ver_respuestas, eliminar_ejercicio, registro, registro_exitoso, autenticacion, ingresar_codigo_acceso, menu_maestro, menu_alumno, logout_view, crear_ejercicio, listar_ejercicios, detalle_ejercicio, subir_respuesta, ver_respuestas, detalle_respuesta, ver_puntajes
from .views import custom_logout
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('login/', login, name='login'),
    path('registro/', registro, name='registro_usuario'),
    path('registro_exitoso/', registro_exitoso, name='registro_exitoso'),
    path('autenticacion/', autenticacion, name='autenticacion'),
    path('ingresar_codigo_acceso/', ingresar_codigo_acceso, name='ingresar_codigo_acceso'),
    path('menu_maestro/', menu_maestro, name='menu_maestro'),
    path('menu_alumno/', menu_alumno, name='menu_alumno'),
    path('logout/', logout_view, name='logout'),
    path('crear_ejercicio/', crear_ejercicio, name='crear_ejercicio'),
    path('listar_ejercicios/', listar_ejercicios, name='listar_ejercicios'),
    path('detalle_ejercicio/<int:ejercicio_id>/', detalle_ejercicio, name='detalle_ejercicio'),
    path('subir_respuesta/<int:ejercicio_id>/', subir_respuesta, name='subir_respuesta'),
    path('ver_respuestas/<int:ejercicio_id>/', ver_respuestas, name='ver_respuestas'),
    path('detalle_respuesta/<int:respuesta_id>/', detalle_respuesta, name='detalle_respuesta'),
    path('ver_puntajes/', ver_puntajes, name='ver_puntajes'),
    path('ver_respuestas/<int:ejercicio_id>/', ver_respuestas, name='ver_respuestas'),
    path('logout/', custom_logout, name='logout'),
    path('captcha/', include('captcha.urls')),
    path('eliminar_ejercicio/<int:ejercicio_id>/', eliminar_ejercicio, name='eliminar_ejercicio'),
    
    
    
    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

