#!/bin/bash

python manage.py runserver 0.0.0.0:8000 &

uvicorn backend_fastapi:app --host 0.0.0.0 --port 8080 --reload &

wait -n

exit $?