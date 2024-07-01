import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ejecutar_codigo():
    try:
        # Código que deseas ejecutar en el sandbox
        logger.info("Ejecutando código en el sandbox")
        
        # Acción visible: crear un archivo
        with open("/code/output.txt", "w") as f:
            f.write("El script se ha ejecutado correctamente.\n")
        
        logger.info("Archivo creado exitosamente.")
    except Exception as e:
        logger.error(f"Error al ejecutar el código: {e}")

if __name__ == "__main__":
    ejecutar_codigo()
