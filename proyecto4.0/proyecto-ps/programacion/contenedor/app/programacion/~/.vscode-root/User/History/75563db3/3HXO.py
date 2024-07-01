

import requests
import random
import string

URL = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s'

def enviar_mensaje(mensaje: str, bot_id: str, chat_id: str) -> bool:
    try:
        respuesta = requests.get(URL % (bot_id, chat_id, mensaje))
        if respuesta.status_code != 200:
            return False
        return True
    except:
        return False

def generar_codigo_verificacion() -> str:
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(random.choice(caracteres) for i in range(8))
    return codigo