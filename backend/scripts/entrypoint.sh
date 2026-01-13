#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Export database URL
export DATABASE_URL=postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:5432/${DB_NAME}

# Decode RSA key if base64 encoded
if [[ ! ${RSA_PRIVATE_KEY} =~ ^----- ]]; then
    export RSA_PRIVATE_KEY=$(echo ${RSA_PRIVATE_KEY} | base64 -d)
fi

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Execute command
exec "$@"
