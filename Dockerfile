# Alpine base image that contains python 3.7
FROM python:3.7-alpine

WORKDIR /srv/python-code-test
COPY . .

# Install system dependencies
# Install pip dependencies in the same layer
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add --no-cache  \
    bash build-base gcc && \
    pip install --no-cache-dir pip-tools==5.2.1 && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
