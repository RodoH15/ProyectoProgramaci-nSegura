

import crypt
import base64
import os

def generar_salt(tamano=12) -> str:
    
    aleatorio = os.urandom(tamano)
    return base64.b64encode(aleatorio).decode('utf-8')

def password_valido(pass_a_evaluar: str, shadow: str) -> bool:
   
    _, algoritmo, salt, resumen = shadow.split('$')
    configuracion = '$%s$%s$' % (algoritmo, salt)
    shadow_nuevo = crypt.crypt(pass_a_evaluar, configuracion)
    return shadow_nuevo == shadow  

def hash_password(password: str) -> str:
    salt = generar_salt()
    configuracion = '$6$%s$' % salt
    return crypt.crypt(password, configuracion)
