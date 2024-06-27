import subprocess
import sys
import json
import os

def decidir_comando(programa: str) -> str:
    partes = programa.split('.')
    if len(partes) > 0:
        if(partes[-1] == 'fasl'):  # sbcl lisp
            programa = 'sbcl --noinform --load %s --quit --disable-debugger --end-toplevel-options $@' % programa
        elif(partes[-1] == 'py'):  # python
            programa = 'python %s' % programa
        elif(partes[-1] == 'prolog'):  # prolog
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

def analizar_codigo(codigo):
    lineas_peligrosas = ['import os', 'import subprocess', 'os.system', 'subprocess.Popen']
    for linea in codigo.split('\n'):
        for peligro in lineas_peligrosas:
            if peligro in linea:
                raise Exception(f'archivo no permitido: {peligro} encontrado')

def inyect(programa, entrada, maxTime=5):
    encoding = sys.getdefaultencoding()
    with open(programa, 'r') as f:
        codigo = f.read()
    
    analizar_codigo(codigo)  # Analizar el código en busca de líneas peligrosas

    programa = decidir_comando(programa)
    log_path = "/code/logs/evaluacion.log"
    with open(log_path, "a") as log_file:
        try:
            log_file.write(f"Ejecutando el programa: {programa} con entrada: {entrada}\n")
            process = subprocess.Popen(programa.split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(input=entrada.encode(), timeout=maxTime)
            output = stdout.decode(encoding)  # 0 es la salida por defecto
            log_file.write(f"Salida: {output}\n")
            log_file.write(f"Errores: {stderr.decode(encoding)}\n")
            if process.returncode != 0:  # un error ocurrió en el proceso hijo
                return ('Runtime error: ' + stderr.decode(encoding), 1)
        except subprocess.TimeoutExpired:  # el proceso está tardando demasiado
            process.kill()  # el proceso debe ser terminado si no se hace sigue corriendo
            log_file.write("Error: Time exceeded\n")
            return ('Time exceeded', 1)
        except Exception as e:
            log_file.write(f"Error: {str(e)}\n")
            return (str(e), 1)  # cualquier error
    return (output, 0)

CASE_BREAK = '$$$$$$'
INPUT_BREAK = '!!!!!!'

def evaluar(programa, arCasos, maxTime=5):
    entrada = ''
    salida = []
    salidaEsperada = ''
    outputEval = False
    res = []
    log_path = "/code/logs/evaluacion.log"
    with open(log_path, "a") as log_file:
        log_file.write(f"Evaluando programa: {programa}\n")
        log_file.write(f"Casos de prueba:\n{arCasos}\n")
        for line in arCasos.splitlines():
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
        log_file.write(f"Resultado de la evaluación: {res}\n")
    return res

if __name__ == '__main__':
    code_path = sys.argv[1]
    casos_de_prueba = sys.argv[2]
    resultado = evaluar(code_path, casos_de_prueba)
    print(json.dumps(resultado))
