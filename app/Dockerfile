FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . .

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt
