#!/usr/bin/env bash

# Install Python dependencies
pip install -r requirements.txt

# Run collectstatic to gather all static files
python manage.py collectstatic --noinput
