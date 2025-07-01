#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create media directory
mkdir -p media
mkdir -p media/profile_pics

# Set permissions for media directory
chmod 755 media
chmod 755 media/profile_pics

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
