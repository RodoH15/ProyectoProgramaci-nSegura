import subprocess
import sys
import json
import os
import logging
import threading
import queue
import uuid

import subprocess
import sys
import json
import os
import logging
from threading import Thread
from queue import Queue

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

task_queue = Queue()
processing = False

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
        resultados = json.loads(result.stdout)
        return calcular_puntaje(resultados)
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {str(e)}")
        print(f"Salida recibida: {result.stdout}")
        raise Exception(f"Error al decodificar JSON: {str(e)} - stdout: {result.stdout}")

def calcular_puntaje(resultados):
    total = len(resultados)
    correctos = resultados.count(True)
    return (correctos / total) * 100 if total > 0 else 0

def add_task_to_queue(task, respuesta_id):
    global processing
    task_id = str(uuid.uuid4())
    task_queue.put((task_id, task, respuesta_id))
    if not processing:
        processing = True
        worker_thread = Thread(target=worker)
        worker_thread.start()
    return task_id

def worker():
    global processing
    while not task_queue.empty():
        task_id, task, respuesta_id = task_queue.get()
        try:
            puntaje = task()
            actualizar_puntaje_respuesta(respuesta_id, puntaje)
            logger.info(f"Tarea {task_id} procesada con éxito. Puntaje: {puntaje}")
        except Exception as e:
            logger.error(f"Error al procesar la tarea {task_id}: {str(e)}")
        task_queue.task_done()
    processing = False

def actualizar_puntaje_respuesta(respuesta_id, puntaje):
    from programacion.models import RespuestaEjercicio
    respuesta = RespuestaEjercicio.objects.get(id=respuesta_id)
    respuesta.puntaje = puntaje
    respuesta.save()
