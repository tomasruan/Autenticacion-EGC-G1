FROM ubuntu:16.04

WORKDIR /app

ADD ./login /app
COPY ./despliegue/requirements.txt /app

ENV MARIADB_HOST g1_mariadb
ENV MARIADB_PORT 3306
ENV MARIADB_USER votaciones-user
ENV MARIADB_PASSWORD votaciones-user-1928

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3 python3-pip libmysqlclient-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "controllers.py"]