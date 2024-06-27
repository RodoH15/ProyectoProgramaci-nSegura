import requests
import sys
import random

# Agregar esta información por usuario como parte de su registro
TOKEN = '7344186903:AAGRtOSxvTq0zDcG5slbsjF3xfFsNNaiReY'
CHAT_ID = '1436880940'

URL = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s'

# Generar código aleatorio de 6 dígitos
codigo = ''.join(random.choices('0123456789', k=8))

def enviar_mensaje(mensaje: str) -> bool:
    """
    Envía el mensaje establecido al bot configurado en las
    variables constantes.

    mensaje: str
    returns: bool, True si se pudo mandar el mensaje, False de lo contrario
    """
    try: 
        respuesta = requests.get(URL %
                                 (TOKEN, CHAT_ID, mensaje))       
        if not respuesta.status_code == 200:
            return False
        return True
    except:
        return False

if __name__ == '__main__':
    mensaje = f'Su código de verificación es: {codigo}'
    if enviar_mensaje(mensaje):
        print('Se mandó el mensaje')
    else:
        print('Hubo un error al mandar el mensaje')


