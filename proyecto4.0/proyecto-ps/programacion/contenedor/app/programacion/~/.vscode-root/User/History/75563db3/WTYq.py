import requests
import random

TOKEN = '7344186903:AAGRtOSxvTq0zDcG5slbsjF3xfFsNNaiReY'
CHAT_ID = '1436880940'

URL = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s'

def enviar_mensaje(mensaje: str) -> bool:
    try:
        respuesta = requests.get(URL % (TOKEN, CHAT_ID, mensaje))
        if respuesta.status_code != 200:
            return False
        return True
    except:
        return False

def generar_codigo_verificacion() -> str:
    return ''.join(random.choices('0123456789', k=8))
