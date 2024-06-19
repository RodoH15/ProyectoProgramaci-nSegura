FROM python:latest

RUN mkdir /code
COPY ./requirements.txt /code
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN pip install python-dotenv
COPY ./start.sh /start/start.sh
RUN chmod +x /start/start.sh

# Crear el directorio staticfiles y ajustar permisos antes de cambiar al usuario limitado
#RUN mkdir -p /code/staticfiles
#RUN chown -R limitado: /code/staticfiles

# Agregar las herramientas necesarias
#RUN apt-get update && apt-get install -y iputils-ping default-mysql-client nano vim

RUN useradd -ms /bin/bash limitado
USER limitado

CMD ["/start/start.sh"]
