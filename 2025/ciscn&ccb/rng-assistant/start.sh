#!/bin/bash

echo "FLAG='$FLAG'" > /app/flag.py

service redis-server start 
redis-cli config set save ""

python3 /app/mini-ollama/default.py &
python3 /app/mini-ollama/math-v1.py &

gunicorn --workers 1 --user=www-data --bind 127.0.0.1:8000 app:app &
nginx

while true; do
    sleep 1
done
