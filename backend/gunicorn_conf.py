from decouple import config

GUNICORN_LOG_LEVEL = config("GUNICORN_LOG_LEVEL", default="INFO")

bind = [
    "0.0.0.0:8000",
]

preload_app = True

workers = 4

chdir = "/usr/src/app/api"

accesslog = "-"

errorlog = "-"

loglevel = GUNICORN_LOG_LEVEL
