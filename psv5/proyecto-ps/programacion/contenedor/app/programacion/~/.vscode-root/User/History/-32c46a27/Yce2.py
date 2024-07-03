import subprocess
import sys
import json
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CASE_BREAK = '$$$$$$'
INPUT_BREAK = '!!!!!!'

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
        for peligro en lineas_peligrosas:
            if peligro en línea:
                raise Exception('Archivo no permitido')

def inyectar(programa, entrada, maxTime=5):
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
            salida = inyectar(programa, entrada, maxTime)
            outputEval = True
            entrada = ''

        elif line == CASE_BREAK:
            outputEval = False
            if salida[1] != 0:
                res.append((salida[0], 1))  # Append error message and error code
            elif salida[0] == salidaEsperada or salida[0].strip() == salidaEsperada.strip():
                res.append((salida[0], 0))  # Correct output
            else:
                res.append((salida[0], 0.5))  # Partial correct output
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

def calcular_puntaje(resultados):
    total = len(resultados)
    correctos = sum(1 for res, status in resultados if status == 0)
    parciales = sum(0.5 for res, status in resultados if status == 0.5)
    return ((correctos + parciales) / total) * 100 if total > 0 else 0

if __name__ == '__main__':
    code_path = sys.argv[1]
    casos_path = sys.argv[2]
    with open(casos_path, 'r') as f:
        casos_de_prueba = f.read()
    resultado = evaluar(code_path, casos_de_prueba)
    print(json.dumps(resultado))
