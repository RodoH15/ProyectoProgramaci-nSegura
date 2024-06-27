FROM python:latest

RUN mkdir /code
COPY ./requirements.txt /code
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


RUN pip install python-dotenv
COPY ./start.sh /start/start.sh
RUN chmod +x /start/start.sh

# Install Docker CLI
RUN apt-get update && \
apt-get install -y docker.io && \
rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash limitado

# Crear el grupo docker solo si no existe y añadir el usuario limitado a este grupo
RUN groupadd -f docker && usermod -aG docker limitado
# Cambiar permisos del socket de Docker


USER limitado
#USER root

CMD ["/start/start.sh"]
