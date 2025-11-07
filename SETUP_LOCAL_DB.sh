#!/bin/bash
# Quick setup script for local PostgreSQL database

echo "Setting up local PostgreSQL database..."

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL not found. Please install it first:"
    echo "  brew install postgresql@16"
    echo "  brew services start postgresql@16"
    echo ""
    echo "Or use Postgres.app: https://postgresapp.com/"
    exit 1
fi

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 &> /dev/null; then
    echo "PostgreSQL is not running. Please start it:"
    echo "  brew services start postgresql@16"
    echo ""
    echo "Or start Postgres.app"
    exit 1
fi

echo "Creating user and database..."

# Create user and database
psql postgres << EOF
-- Create user if it doesn't exist
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'invest') THEN
        CREATE USER invest WITH PASSWORD 'invest';
    END IF;
END
\$\$;

-- Create database if it doesn't exist
SELECT 'CREATE DATABASE investdb OWNER invest'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'investdb')\gexec

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE investdb TO invest;
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Database 'investdb' and user 'invest' created successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Copy .env.local to .env: cp .env.local .env"
    echo "2. Run migrations: cd backend && python3 -m alembic revision --autogenerate -m 'init'"
    echo "3. Apply migrations: python3 -m alembic upgrade head"
else
    echo "❌ Failed to create database. Please check PostgreSQL is running."
    exit 1
fi

