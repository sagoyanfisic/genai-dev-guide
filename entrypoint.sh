#!/bin/bash
set -e

echo "🚀 Starting PDF AI App..."

# Wait for database to be ready
echo "⏳ Waiting for database connection..."
until nc -z ${DB_HOST:-mariadb} ${DB_PORT:-3306}; do
    echo "Database not ready yet, waiting..."
    sleep 2
done
echo "✅ Database is ready!"

# Run migrations
echo "🔄 Running database migrations..."
uv run alembic upgrade head
echo "✅ Migrations completed!"

# Start the application
echo "🌟 Starting Granian server (Rust-powered ASGI)..."
uv run granian --host 0.0.0.0 --port 8000 --workers 2 --interface asgi app.main:app
