#!/bin/sh

# Explicit wait, so migration will be performed after DB start
sleep 5

python3 got_api/manage.py collectstatic --no-input --clear
python3 got_api/manage.py migrate
python3 got_api/manage.py upload_episodes_to_db

exec "$@"
