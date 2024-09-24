#!/usr/bin/env bash

python manage.py migrate

echo "Executing entrypoint!"
exec "$@"
