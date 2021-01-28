#!/bin/bash

#gunicorn --log-level info --log-file=/gunicorn.log --workers 4 --name app -b 0.0.0.0:8000 --reload app.app:app
export FLASK_APP=app:app
flask db upgrade
gunicorn -c gunicorn_config.py app:app
