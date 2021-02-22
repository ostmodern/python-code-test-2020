# Alpine base image that contains python 3.7
FROM python:3.7-alpine

WORKDIR /srv/python-code-test
COPY requirements.txt .
COPY . .

# Install system dependencies
# Install pip dependencies in the same layer
RUN apk add --no-cache  \
    bash build-base gcc postgresql-dev && \
    pip install --no-cache-dir pip-tools==5.2.1 && \
    pip install --no-cache-dir -r requirements.txt

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/srv/python-code-test/entrypoint.sh"]
