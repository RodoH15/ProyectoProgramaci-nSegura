# scripts.py
import sys
import subprocess

def decidir_comando(programa: str) -> str:
    partes = programa.split('.') 
    if len(partes) > 0:
        if(partes[-1] == 'fasl'):
            programa = 'sbcl --noinform --load %s --quit --disable-debugger --end-toplevel-options $@' % programa
        elif(partes[-1] == 'py'):
            programa = 'python %s' % programa
        elif(partes[-1] == 'prolog'):
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
    encoding = sys.getdefaultencoding()
    programa = decidir_comando(programa)
    try:
        process = subprocess.Popen(programa.split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        tup = process.communicate(bytes(entrada, encoding), maxTime)
        output = str(tup[0], encoding)
        if process.returncode != 0:
            return ('Runtime error', 1)
    except subprocess.TimeoutExpired:
        process.kill()
        return ('Time exceeded', 1)
    except Exception as err:
        return (sys.exc_info()[0], 1)
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
