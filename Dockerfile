FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/user
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt --upgrade pip && pip install gunicorn

COPY . /home/user

ENTRYPOINT ["./runserver.sh"]
