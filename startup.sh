#!/bin/bash
# Azure App Service startup script for Voice Assisted KidzAgent

echo "Starting Voice Assisted KidzAgent..."

# Navigate to app directory
cd /home/site/wwwroot

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized')" || echo "Database initialization warning (may already exist)"

# Start gunicorn
echo "Starting Gunicorn..."
exec gunicorn --bind=0.0.0.0 --workers=4 --worker-class=sync --timeout=60 --access-logfile - --error-logfile - run:app
