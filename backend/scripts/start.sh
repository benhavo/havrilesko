#!/bin/bash

set -eo pipefail

# Run with uvicorn directly (development)
if [ "$BUILD_ENV" = "local" ]; then
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
    # Production: use uvicorn with multiple workers
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
fi
