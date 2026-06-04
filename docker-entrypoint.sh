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

# Wait for Redis to be ready
if [ "$REDIS_HOST" ]; then
    echo "Waiting for Redis at $REDIS_HOST:${REDIS_PORT:-6379}..."
    while ! nc -z $REDIS_HOST ${REDIS_PORT:-6379}; do
      sleep 0.5
    done
    echo "Redis is ready!"
fi

# Run database migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Compile translation files
echo "Compiling translation files..."
if [ -d "locale" ] && find locale -name "*.po" 2>/dev/null | grep -q .; then
    python manage.py compilemessages
else
    echo "No translation source files (.po) found. Skipping compilation."
fi

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
