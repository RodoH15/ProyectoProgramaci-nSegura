FROM python:latest

RUN mkdir /code
COPY ./requirements.txt /code
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


RUN pip install python-dotenv
COPY ./start.sh /start/start.sh
RUN chmod +x /start/start.sh

RUN apt-get update && apt-get install -y docker.io && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash limitado
RUN groupadd -g 999 docker || true && usermod -aG docker limitado
USER limitado
#USER root

CMD ["/start/start.sh"]
