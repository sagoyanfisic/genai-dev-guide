#!/bin/bash
set -e

echo "🚀 Starting PDF AI App..."

# Check if we're using Cloud SQL or MariaDB
if [ "${USE_CLOUD_SQL:-false}" = "true" ]; then
    echo "🌩️ Using Cloud SQL - no database health check needed"
    echo "📊 Configuration:"
    echo "   Instance: ${CLOUD_SQL_INSTANCE_CONNECTION_NAME}"
    echo "   IAM Auth: ${USE_IAM_AUTH:-false}"
    echo "   Database: ${DB_NAME}"
else
    # Wait for MariaDB to be ready
    echo "🐬 Using MariaDB - waiting for database connection..."
    until nc -z ${DB_HOST:-mariadb} ${DB_PORT:-3306}; do
        echo "Database not ready yet, waiting..."
        sleep 2
    done
    echo "✅ MariaDB is ready!"
fi

# Run migrations
echo "🔄 Running database migrations..."
uv run alembic upgrade head
echo "✅ Migrations completed!"

# Start the application
echo "🌟 Starting Granian server (Rust-powered ASGI)..."
uv run granian --host 0.0.0.0 --port 8000 --workers 2 --interface asgi app.main:app
