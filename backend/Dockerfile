ARG PYTHON_VERSION=3.12-slim-bookworm

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} AS python

# Python build stage
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=production

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev

# Requirements are installed here to ensure they will be cached.
COPY ./requirements .

# Get latest pip
RUN pip install --upgrade pip

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r ${BUILD_ENVIRONMENT}.txt

# Python 'run' stage
FROM python AS python-run-stage

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV BUILD_ENV=${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN addgroup --system fastapi \
    && adduser --system --ingroup fastapi fastapi

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

COPY --chown=fastapi:fastapi ./scripts/passthru.sh /passthru.sh
RUN sed -i 's/\r$//g' /passthru.sh
RUN chmod +x /passthru.sh

COPY --chown=fastapi:fastapi ./scripts/migrate.sh /migrate.sh
RUN sed -i 's/\r$//g' /migrate.sh
RUN chmod +x /migrate.sh

COPY --chown=fastapi:fastapi ./scripts/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY --chown=fastapi:fastapi ./scripts/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

# copy application code to WORKDIR
COPY --chown=fastapi:fastapi . ${APP_HOME}

# make fastapi owner of the WORKDIR directory as well.
RUN chown fastapi:fastapi ${APP_HOME}

USER fastapi

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]
