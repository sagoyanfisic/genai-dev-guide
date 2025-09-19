#!/bin/bash
set -e

echo "🚀 Starting PDF AI App..."

# Wait for MariaDB to be ready
echo "🐬 Using MariaDB - waiting for database connection..."
until nc -z ${DB_HOST} ${DB_PORT:-3306}; do
    echo "Database not ready yet, waiting..."
    sleep 2
done
echo "✅ MariaDB is ready!"

# Run migrations
echo "🔄 Running database migrations..."
uv run alembic upgrade head
echo "✅ Migrations completed!"

# Start the application
echo "🌟 Starting Granian server (Rust-powered ASGI)..."
uv run granian --host 0.0.0.0 --port 8080 --workers 2 --interface asgi app.main:app
