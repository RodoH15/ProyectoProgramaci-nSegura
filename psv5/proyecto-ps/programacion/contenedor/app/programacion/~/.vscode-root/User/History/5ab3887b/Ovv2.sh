#!/bin/bash

# Mantener el contenedor activo
tail -f /dev/null

# Ejecutar el script sandbox.py
python /code/programacion/scripts/sandbox.py

# Mantener el contenedor corriendo para otros propósitos
exec "$@"
