FROM python:3.9.1-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG ROOT_DIR=/app

WORKDIR /app

RUN apt-get update && apt-get install -y netcat

COPY ./requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip && pip install -r /app/requirements.txt

COPY api/src/ /app

COPY api/support/wait-services.sh /app
RUN chmod +x wait-services.sh

ENTRYPOINT ["./wait-services.sh", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app"]