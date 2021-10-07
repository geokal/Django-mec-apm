FROM python:3.8.5-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install — upgrade pip && pip install python3-dev && pip3 install mysqlclient
RUN pip install -r requirements.txt
RUN apt-get install netcat
ADD . /code/
COPY wait.sh /wait.sh
RUN chmod +x /wait.sh