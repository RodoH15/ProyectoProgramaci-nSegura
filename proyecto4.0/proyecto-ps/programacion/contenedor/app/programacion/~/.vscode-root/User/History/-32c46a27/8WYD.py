import subprocess
import sys
import json
import os
import logging
import uuid
from threading import Thread, Lock
from queue import Queue as ThreadQueue
from programacion.models import RespuestaEjercicio

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Crear una cola en memoria y un lock para asegurar la sincronización
task_queue = ThreadQueue()
queue_lock = Lock()

def decidir_comando(programa: str) -> str:
    logger.debug(f"Decidiendo comando para: {programa}")
    partes = programa.split('.')
    if len(partes) > 0:
        if partes[-1] == 'fasl':  # sbcl lisp
            programa = 'sbcl --noinform --load %s --quit --disable-debugger --end-toplevel-options $@' % programa
        elif partes[-1] == 'py':  # python
            programa = 'python %s' % programa
        elif partes[-1] == 'prolog':  # prolog
            programa = 'swipl -f %s -t main -q' % programa
        elif partes[-1] == 'class':
            programa = programa[:programa.index('.class')]
            pps = programa.split('/')
            dire = ''
            for pp in pps[:-1]:
                dire += (pp + '/')
            programa = pps[-1]
            programa = 'java -cp %s %s' % (dire, programa)
    return programa

def analizar_codigo(codigo):
    logger.debug("Analizando código...")
    lineas_peligrosas = ['import os', 'import subprocess', 'os.system', 'subprocess.Popen']
    for linea in codigo.split('\n'):
        for peligro in lineas_peligrosas:
            if peligro in linea:
                raise Exception('Archivo no permitido')

def inyect(programa, entrada, maxTime=5):
    logger.debug(f"Inyectando entrada: {entrada} en programa: {programa}")
    encoding = sys.getdefaultencoding()
    with open(programa, 'r') as f:
        codigo = f.read()

    analizar_codigo(codigo)
    programa = decidir_comando(programa)
    
    try:
        process = subprocess.Popen(programa.split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=entrada.encode(), timeout=maxTime)
        output = stdout.decode(encoding)
        if process.returncode != 0:
            return ('Runtime error: ' + stderr.decode(encoding), 1)
    except subprocess.TimeoutExpired:
        process.kill()
        return ('Time exceeded', 1)
    except Exception as e:
        return (str(e), 1)
    return (output, 0)

CASE_BREAK = '$$$$$$'
INPUT_BREAK = '!!!!!!'

def evaluar(programa, arCasos, maxTime=5):
    entrada = ''
    salida = []
    salidaEsperada = ''
    outputEval = False
    res = []
    for line in arCasos.splitlines():
        messyLine = line
        line = line.strip()

        if line == CASE_BREAK and salida == []:
            continue

        if line == '':
            continue

        if line == INPUT_BREAK:
            salida = inyect(programa, entrada, maxTime)
            outputEval = True
            entrada = ''

        elif line == CASE_BREAK:
            outputEval = False
            if salida[1] != 0:
                res.append(salida[0])
            elif salida[0] == salidaEsperada or salida[0].strip() == salidaEsperada.strip():
                res.append(True)
            else:
                res.append(False)
            salidaEsperada = ''

        elif outputEval:
            salidaEsperada += messyLine

        else:
            if line.strip().startswith('['):
                entrada += line + '\n'
            else:
                for elem in line.split(','):
                    entrada += elem + '\n'

    return res

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
    correctos = resultados.count(True)
    return (correctos / total) * 100 if total > 0 else 0

def actualizar_puntaje_respuesta(respuesta_id, puntaje):
    from programacion.models import RespuestaEjercicio
    respuesta = RespuestaEjercicio.objects.get(id=respuesta_id)
    respuesta.puntaje = puntaje
    respuesta.save()

def procesar_tarea(code_path, casos_path, respuesta_id):
    try:
        resultados = evaluar_con_casos_directos(code_path, casos_path)
        puntaje = calcular_puntaje(resultados)
        actualizar_puntaje_respuesta(respuesta_id, puntaje)
        logger.info(f"Tarea procesada exitosamente. Puntaje: {puntaje}")
    except Exception as e:
        logger.error(f"Error al procesar la tarea: {e}")

def worker():
    while True:
        task = task_queue.get()
        if task is None:
            break
        code_path, casos_path, respuesta_id = task
        procesar_tarea(code_path, casos_path, respuesta_id)
        task_queue.task_done()

# Iniciar el worker en un hilo separado
worker_thread = Thread(target=worker)
worker_thread.daemon = True
worker_thread.start()

def add_task_to_queue(code_path, casos_path, respuesta_id):
    task_id = str(uuid.uuid4())
    with queue_lock:
        task_queue.put((code_path, casos_path, respuesta_id))
    return task_id

if __name__ == '__main__':
    code_path = sys.argv[1]
    casos_path = sys.argv[2]
    respuesta_id = sys.argv[3]
    add_task_to_queue(code_path, casos_path, respuesta_id)
