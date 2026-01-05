#!/bin/bash
set -e

# Generate certificates if they don't exist
if [ ! -f cert.pem ] || [ ! -f key.pem ]; then
    echo "Generating self-signed certificates..."
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
fi

echo "Starting server..."
# Using python from venv
./venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 5000 --ssl-keyfile key.pem --ssl-certfile cert.pem
