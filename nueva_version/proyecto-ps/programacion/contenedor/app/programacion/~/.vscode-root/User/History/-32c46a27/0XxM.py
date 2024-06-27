# scripts.py
import subprocess
import sys

def decidir_comando(programa: str) -> str:
    """
    Dependiendo del lenguaje de programación,
    determina el comando que se debe ejecutar

    programa: path de un archivo de entrada con extensión
    returns: str, comando usado para ejecutar el programa
    """
    partes = programa.split('.') 
    if len(partes) > 0:
        if(partes[-1] == 'fasl'): #sbcl lisp
            programa = 'sbcl --noinform --load %s --quit --disable-debugger --end-toplevel-options $@' % programa
        elif(partes[-1] == 'py'): #python
            programa = 'python %s' % programa
        elif(partes[-1] == 'prolog'): #prolog
            programa = 'swipl -f %s -t main -q' % programa
        elif(partes[-1] == 'class'):
            programa = programa[:programa.index('.class')]
            pps = programa.split('/')
            dire = ''
            for pp in pps[:-1]:
                dire += (pp + '/')
            programa = pps[-1]
            programa = 'java -cp %s %s' % (dire, programa)
    return programa

def inyect(programa, entrada, maxTime=5):
    """
    Inyecta una entrada a un programa dado y regresa una tupla con la salida y un codigo de salida
    Hace un chequeo para saber si ejecutarlo con un interprete
    """
    encoding = sys.getdefaultencoding()
    programa = decidir_comando(programa)
    try:
        process = subprocess.Popen(programa.split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        tup = process.communicate(bytes(entrada, encoding), maxTime)
        output = str(tup[0], encoding) #0 es la salida por defecto
        if process.returncode != 0: #an error ocurred in child process
            return ('Runtime error', 1)
    except subprocess.TimeoutExpired: #the process is taking too long
        process.kill() #the process must be killed if don't it keps running
        return ('Time exceeded', 1)
    except Exception as err:        
        return (sys.exc_info()[0], 1) #any error
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

        if(line == CASE_BREAK and salida == []):
            continue

        if(line == ''):
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
