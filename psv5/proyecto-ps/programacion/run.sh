
#!/usr/bin/env bash

activado=''
while read -r line; do
    activado='1'
    export "$line"
done < <(ccdecrypt -c secrets.env.cpt)

test "$activado" || { echo "No se pasó correctamente la contraseña"; exit 1; } 

docker-compose up --build
#python3 manage.py runserver



