import subprocess
import sys
import json
import os
import logging
from threading import Thread
from queue import Queue

# Configuración de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

task_queue = Queue()

def worker():
    while True:
        task = task_queue.get()
        if task is None:
            break
        code_path, casos_path = task
        logger.debug(f"Procesando tarea con código en {code_path} y casos de prueba en {casos_path}")
        try:
            result = evaluar_con_casos_directos(code_path, casos_path)
            puntaje = calcular_puntaje(result)
            logger.info(f"Tarea procesada exitosamente. Puntaje: {puntaje}")
        except Exception as e:
            logger.error(f"Error al procesar la tarea: {e}")
        task_queue.task_done()

def add_task_to_queue(code_path, casos_path):
    task_queue.put((code_path, casos_path))
    logger.info(f"Tarea añadida a la cola con código en {code_path}")

def evaluar_con_casos_directos(code_path, casos_path):
    comando = f"docker exec -i programacion-programacion-executor-1-1 python3 /code/programacion/scripts/scripts.py {code_path} {casos_path}"
    result = subprocess.run(comando, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Error al ejecutar el comando: {result.stderr}")

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise Exception(f"Error al decodificar JSON: {str(e)} - stdout: {result.stdout}")

def calcular_puntaje(resultados):
    total = len(resultados)
    correctos = sum(1 for r in resultados if r)
    return (correctos / total) * 100 if total > 0 else 0

# Inicia el worker en un thread
worker_thread = Thread(target=worker)
worker_thread.start()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: scripts.py <code_path> <casos_path>")
        sys.exit(1)

    code_path = sys.argv[1]
    casos_path = sys.argv[2]
    
    add_task_to_queue(code_path, casos_path)
