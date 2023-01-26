# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#Nao precisa mais copiar pq vamos usar o codido de dev na maquina host
#COPY . .
CMD ["pymon","mysource.py"]