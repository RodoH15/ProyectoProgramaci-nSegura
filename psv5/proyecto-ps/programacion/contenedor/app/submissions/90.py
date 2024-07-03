# suma_parcial.py
a = int(input())
b = int(input())

# Condición que altera uno de los resultados esperados para los casos de prueba
if a == 2 and b == 2:
    print(a + b + 1)  # Devuelve 5 en lugar de 4
else:
    print(a + b)