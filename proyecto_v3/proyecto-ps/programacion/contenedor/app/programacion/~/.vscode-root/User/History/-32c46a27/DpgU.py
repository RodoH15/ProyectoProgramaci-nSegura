import subprocess
import sys

def decidir_comando(programa: str) -> str:
    partes = programa.split('.')
    if len(partes) > 0:
        if partes[-1] == 'fasl':  # sbcl lisp
            return f'sbcl --noinform --load {programa} --quit --disable-debugger --end-toplevel-options $@'
        elif partes[-1] == 'py':  # python
            return f'python {programa}'
        elif partes[-1] == 'prolog':  # prolog
            return f'swipl -f {programa} -t main -q'
        elif partes[-1] == 'class':  # java
            programa = programa[:programa.index('.class')]
            pps = programa.split('/')
            dire = '/'.join(pps[:-1])
            programa = pps[-1]
            return f'java -cp {dire} {programa}'
    return programa

def analizar_codigo(codigo):
    lineas_peligrosas = ['import os', 'import subprocess', 'os.system', 'subprocess.Popen']
    for linea in codigo.split('\n'):
        for peligro in lineas_peligrosas:
            if peligro in linea:
                raise Exception(f'archivo no permitido')

def inyectar(programa, entrada, maxTime=5):
    encoding = sys.getdefaultencoding()
    with open(programa, 'r') as f:
        codigo = f.read()
    
    analizar_codigo(codigo)  # Analizar el código en busca de líneas peligrosas

    comando = decidir_comando(programa)
    contenedor = "programacion_executor_1"  # Nombre del contenedor ejecutor

    try:
        process = subprocess.Popen(
            ["docker", "exec", contenedor, "bash", "-c", comando], 
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        tup = process.communicate(bytes(entrada, encoding), timeout=maxTime)
        output = str(tup[0], encoding)
        if process.returncode != 0:
            return ('Runtime error: ' + str(tup[1], encoding), 1)
    except subprocess.TimeoutExpired:
        process.kill()
        return ('Time exceeded', 1)
    except Exception as err:
        return (str(err), 1)
    
    return (output, 0)

CASE_BREAK = '$$$$$$'
INPUT_BREAK = '!!!!!!'

def evaluar(programa, arCasos, maxTime=5):
    entrada = ''
    salida = []
    salidaEsperada = ''
    outputEval = False
    res = []
    for line in open(arCasos):
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

if __name__ == "__main__":
    programa = sys.argv[1]
    arCasos = sys.argv[2]
    maxTime = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    print(evaluar(programa, arCasos, maxTime))
