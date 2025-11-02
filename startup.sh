#!/bin/bash

echo "Starting CIMB Anti-Scam Dashboard on Azure App Service..."

# Install Python dependencies
pip install -r requirements-azure.txt

# Start Gunicorn
gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app
