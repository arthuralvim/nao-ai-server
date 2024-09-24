FROM python:3.12-slim

ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_ROOT_USER_ACTION=ignore \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.8.3 \
  POETRY_HOME="/opt/poetry" \
  PATH="$POETRY_HOME/bin:/usr/src/backend/bin:${PATH}"

RUN \
  apt-get update && apt-get install -y \
  bash \
  tini \
  && rm -rf /var/lib/apt/lists/*

RUN pip install poetry=="$POETRY_VERSION"

COPY ../../backend/poetry.lock ../../backend/pyproject.toml /usr/src/backend/
WORKDIR /usr/src/backend
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root

COPY ../../backend /usr/src/backend
WORKDIR /usr/src/backend

EXPOSE 8000
ENTRYPOINT ["/usr/bin/tini", "--", "docker-entrypoint.sh"]
CMD ["docker-cmd.sh"]
