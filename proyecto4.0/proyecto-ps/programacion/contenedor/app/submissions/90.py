def suma(a, b):
    return a + b

if __name__ == "__main__":
    import sys
    input_data = sys.stdin.read().split()
    a = int(input_data[0])  # Cambiado a [0]
    b = int(input_data[1])  # Cambiado a [1]
    print(suma(a, b))
