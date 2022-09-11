FROM python:3.10.7-alpine3.16

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN \
 apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

COPY ./requirements.txt /src
RUN python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY ./src/ .

RUN addgroup -S web && adduser -S web -G web \
    && chown web:web -R /src
USER web

ENTRYPOINT ["/src/entrypoint.sh"]