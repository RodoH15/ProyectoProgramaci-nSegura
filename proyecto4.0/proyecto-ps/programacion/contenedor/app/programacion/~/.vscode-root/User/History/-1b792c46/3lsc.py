import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ejecutar_codigo():
    try:
        # Código que deseas ejecutar en el sandbox
        logger.info("Ejecutando código en el sandbox")
        # Aquí va el código a ejecutar
    except Exception as e:
        logger.error(f"Error al ejecutar el código: {e}")

if __name__ == "__main__":
    ejecutar_codigo()