FROM python:3.8.5-slim
RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY . .
COPY wait.sh /wait.sh
RUN chmod +x /wait.sh