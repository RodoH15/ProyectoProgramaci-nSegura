import subprocess
import sys
import json
import os
import logging
import threading
import queue
import uuid

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cola de tareas
task_queue = queue.Queue()
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
            for pp en pps[:-1]:
                dire += (pp + '/')
            programa = pps[-1]
            programa = 'java -cp %s %s' % (dire, programa)
    return programa

def analizar_codigo(codigo):
    logger.debug("Analizando código...")
    lineas_peligrosas = ['import os', 'import subprocess', 'os.system', 'subprocess.Popen']
    para linea en codigo.split('\n'):
        para peligro en lineas_peligrosas:
            si peligro en linea:
                raise Exception('Archivo no permitido')

def inyect(programa, entrada, maxTime=5):
    logger.debug(f"Inyectando entrada: {entrada} en programa: {programa}")
    encoding = sys.getdefaultencoding()
    con open(programa, 'r') como f:
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
    para linea en arCasos.splitlines():
        messyLine = linea
        linea = linea.strip()

        if linea == CASE_BREAK y salida == []:
            continuar

        if linea == '':
            continuar

        if linea == INPUT_BREAK:
            salida = inyect(programa, entrada, maxTime)
            outputEval = True
            entrada = ''

        elif linea == CASE_BREAK:
            outputEval = False
            if salida[1] != 0:
                res.append(salida[0])
            elif salida[0] == salidaEsperada o salida[0].strip() == salidaEsperada.strip():
                res.append(True)
            else:
                res.append(False)
            salidaEsperada = ''

        elif outputEval:
            salidaEsperada += messyLine

        else:
            if linea.strip().startswith('['):
                entrada += linea + '\n'
            else:
                para elem en linea.split(','):
                    entrada += elem + '\n'

    return res

def add_task_to_queue(task):
    global processing
    task_id = str(uuid.uuid4())
    task_queue.put((task_id, task))
    if not processing:
        processing = True
        worker_thread = threading.Thread(target=worker)
        worker_thread.start()
    return task_id

def worker():
    global processing
    while not task_queue.empty():
        task_id, task = task_queue.get()
        try:
            task()
        except Exception as e:
            logger.error(f"Error al procesar la tarea {task_id}: {str(e)}")
        finally:
            task_queue.task_done()
    processing = False

def evaluar_con_casos_directos(code_path, casos_path, respuesta_id):
    comando = f"docker exec -i programacion-programacion-executor-1-1 python3 /code/programacion/scripts/scripts.py {code_path} {casos_path}"
    result = subprocess.run(comando, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"Error al ejecutar el comando: {result.stderr}")

    try:
        resultados = json.loads(result.stdout)
        actualizar_puntaje_respuesta(respuesta_id, calcular_puntaje(resultados))
    except json.JSONDecodeError as e:
        raise Exception(f"Error al decodificar JSON: {str(e)} - stdout: {result.stdout}")

def actualizar_puntaje_respuesta(respuesta_id, puntaje):
    from programacion.models import RespuestaEjercicio
    respuesta = RespuestaEjercicio.objects.get(id=respuesta_id)
    respuesta.puntaje = puntaje
    respuesta.save()

def calcular_puntaje(resultados):
    total = len(resultados)
    correctos = resultados.count(True)
    return (correctos / total) * 100 if total > 0 else 0

if __name__ == '__main__':
    code_path = sys.argv[1]
    casos_path = sys.argv[2]
    con open(casos_path, 'r') como f:
        casos_de_prueba = f.read()
    resultado = evaluar(code_path, casos_de_prueba)
    print(json.dumps(resultado))