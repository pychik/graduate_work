FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev make \
    && rm -rf /var/lib/apt/lists/*


COPY ./auth/requirements.txt /app
RUN python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt --no-cache-dir
COPY ./auth/src /app
COPY ./auth/tests tests/

ENV PYTHONPATH=.

ENTRYPOINT ["/app/entrypoint.sh"]