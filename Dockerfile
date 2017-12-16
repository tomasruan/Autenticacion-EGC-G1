FROM ubuntu:16.04

WORKDIR /app

ADD ./login /app
COPY ./despliegue/requirements.txt /app


RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3 python3-pip libmysqlclient-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "controllers.py"]