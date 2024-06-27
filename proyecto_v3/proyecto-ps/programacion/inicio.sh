#!/usr/bin/env bash

# Verificar si el archivo .env.cpt existe
if [ ! -f "/root/proyecto-ps/programacion/.env.cpt" ]; then
    echo "El archivo .env.cpt no existe."
    exit 1
fi

# Descifrar el archivo .env.cpt
ccdecrypt /root/proyecto-ps/programacion/.env.cpt
if [ $? -ne 0 ]; then
    echo "Error al descifrar el archivo .env.cpt."
    exit 1
fi

# Verificar si el archivo .env fue creado correctamente
if [ ! -f "/root/proyecto-ps/programacion/.env" ]; then
    echo "El archivo .env no fue creado."
    exit 1
fi

# Cargar variables de entorno desde el archivo .env
set -o allexport
source /root/proyecto-ps/programacion/.env
set -o allexport

# Eliminar el archivo .env después de cargarlo
rm /root/proyecto-ps/programacion/.env

cd /root/proyecto-ps/programacion
python3 manage.py check
python3 manage.py runserver
