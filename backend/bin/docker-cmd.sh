#!/usr/bin/env bash

set -o errexit
set -o nounset
set -x

exec "/usr/local/bin/gunicorn" \
  "--config=/usr/src/backend/gunicorn_conf.py" \
  "hackathon_nao.wsgi"
