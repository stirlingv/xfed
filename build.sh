#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Load initial content (optional - uncomment when you have fixtures)
# python manage.py loaddata fixtures/site_content.json

# Load navigation content (uncomment after running migrations)
# python manage.py loaddata fixtures/navigation.json
