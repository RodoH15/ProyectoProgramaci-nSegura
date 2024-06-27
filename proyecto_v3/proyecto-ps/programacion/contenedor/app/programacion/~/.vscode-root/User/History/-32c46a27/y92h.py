# scripts.py
import sys
import subprocess

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
            return ('Runtime error',1)
    except subprocess.TimeoutExpired: #the process is taking too long
        process.kill() #the process must be killed if don't it keps running
        return ('Time exceeded',1)
    except Exception as err:        
        return (sys.exc_info()[0], 1) #any error
    return (output,0) # 0 means no errors







CASE_BREAK = '$$$$$$'
INPUT_BREAK = '!!!!!!'

def evaluar(programa, arCasos, maxTime=5):
    """
    Programa ya es el compilado o script
    maxTime es para establecer en segundos el tiempo máximo de ejecución
    Cada caso se separa por la cadena especiasl $$$$$$$
    La entrada se separa de la salida por la cadena especial !!!!!!
    """
    entrada = '' #la cadena total que se enviara
    salida = [] #para tenerla declarada por si el scope
    salidaEsperada = '' #para ir guardando lo que se lee en el archivo
    outputEval = False #se activa cuando se evalua el output
    res = []  #para guardar los resultados de cada caso
    for line in open(arCasos):
        messyLine = line #no quitar saltos de línea ni nada, para comparar con salida esperada (tienen que ser exactametne iguales)
        line = line.strip() #quitar saltos de línea al final así como espacios extra, para evitar posibles errores en el input y facilitar el proceso

        if(line == CASE_BREAK and salida == []): #es la primera línea
            continue

        if(line == ''): #ignorar líneas vacías
            continue

        if line == INPUT_BREAK: #dejar de llenar la entrada he inyectar
            
            salida = inyect(programa, entrada, maxTime)
            outputEval = True
            entrada = '' #restart input

        elif line == CASE_BREAK: #cambiar banderas y evaluar
            outputEval = False
            if salida[1] != 0: # 0 es sin errores
                res.append(salida[0]) #el tipo de error
            elif salida[0] == salidaEsperada or salida[0].strip() == salidaEsperada.strip(): #sometimes the new lines must be preserved
                res.append(True)
            else:
                res.append(False)
            salidaEsperada = '' #restart output

        elif outputEval:
            salidaEsperada += messyLine

        else: #input reconstruction
            if line.strip().startswith('['): #si es una lista prolog no se quieren saltos de linea
                entrada += line + '\n'
            else:
                for elem in line.split(','):
                    entrada += elem + '\n'

    return res
