# Alpine base image that contains python 3.7
FROM python:3.6-alpine

WORKDIR /srv/python-code-test

RUN mkdir -p /srv/python-code-test/omdb
RUN mkdir -p /srv/python-code-test/scripts

COPY requirements.txt .

COPY omdb /srv/python-code-test/omdb
COPY scripts /srv/python-code-test/scripts

# Install system dependencies
# Install pip dependencies in the same layer
RUN apk add --no-cache  \
    postgresql-dev \
    bash build-base gcc && \
    pip install --no-cache-dir pip-tools==5.2.1 && \
    pip install --no-cache-dir -r requirements.txt

RUN chmod +x /srv/python-code-test/scripts/*

EXPOSE 8000

CMD ./scripts/start.sh