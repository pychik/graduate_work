FROM python:3.9.7-alpine

WORKDIR /usr/src/etl

ENV PYTHON_PATH=.

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN echo $PATH

COPY . /usr/src/etl/

#CMD ['python', 'main.py']
