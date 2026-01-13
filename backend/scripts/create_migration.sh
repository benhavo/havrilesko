#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

echo "Creating migration..."
alembic revision --autogenerate -m "${1:-Initial migration}"
