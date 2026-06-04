#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for PostgreSQL to be ready
if [ "$DB_HOST" ]; then
    echo "Waiting for database at $DB_HOST:${DB_PORT:-5432}..."
    while ! nc -z $DB_HOST ${DB_PORT:-5432}; do
      sleep 0.5
    done
    echo "Database is ready!"
fi

# Run database migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Load demo data if requested
if [ "$LOAD_DEMO_DATA" = "true" ]; then
    echo "Loading demo data..."
    python manage.py load_demo_data
fi

# Execute the main container command
exec "$@"
