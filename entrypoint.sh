#!/bin/bash
set -e

echo "🚀 Starting PDF AI App..."

# Wait for database to be ready
echo "⏳ Waiting for database connection..."
until mysql -h"${DB_HOST:-mariadb}" -u"${DB_USER:-pdf_user}" -p"${DB_PASSWORD:-pdf_password}" -e "SELECT 1" >/dev/null 2>&1; do
  echo "Database not ready yet, waiting..."
  sleep 2
done
echo "✅ Database is ready!"

# Run migrations
echo "🔄 Running database migrations..."
alembic upgrade head
echo "✅ Migrations completed!"

# Start the application
echo "🌟 Starting Gunicorn server..."
exec gunicorn --config gunicorn.conf.py app.main:app