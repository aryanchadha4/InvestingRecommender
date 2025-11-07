#!/usr/bin/env python3
"""Create PostgreSQL database and user using psycopg."""

import psycopg
from psycopg import sql

# Connect as the default postgres user (usually your macOS username)
# This connection will work without specifying user/password for local connections
try:
    # Try connecting with default user
    conn = psycopg.connect("dbname=postgres")
except Exception as e:
    print(f"Error connecting: {e}")
    print("\nPlease run this command manually in your terminal:")
    print("psql postgres")
    print("\nThen run these SQL commands:")
    print("CREATE USER invest WITH PASSWORD 'invest';")
    print("CREATE DATABASE investdb OWNER invest;")
    print("GRANT ALL PRIVILEGES ON DATABASE investdb TO invest;")
    exit(1)

conn.autocommit = True
cur = conn.cursor()

try:
    # Create user if it doesn't exist
    cur.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'invest') THEN
                CREATE USER invest WITH PASSWORD 'invest';
                RAISE NOTICE 'User invest created';
            ELSE
                RAISE NOTICE 'User invest already exists';
            END IF;
        END
        $$;
    """)
    print("✅ User 'invest' created or already exists")
    
    # Create database if it doesn't exist
    cur.execute("""
        SELECT 'CREATE DATABASE investdb OWNER invest'
        WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'investdb')
    """)
    result = cur.fetchone()
    if result:
        cur.execute(result[0])
        print("✅ Database 'investdb' created")
    else:
        print("✅ Database 'investdb' already exists")
    
    # Grant privileges
    cur.execute("GRANT ALL PRIVILEGES ON DATABASE investdb TO invest;")
    print("✅ Privileges granted")
    
    # Verify
    cur.execute("SELECT datname, datdba::regrole FROM pg_database WHERE datname = 'investdb'")
    db_info = cur.fetchone()
    if db_info:
        print(f"\n✅ Database verified: {db_info[0]} (owner: {db_info[1]})")
    
    print("\n🎉 Database setup complete!")
    print("\nNext steps:")
    print("1. cd backend")
    print("2. python3 -m alembic revision --autogenerate -m 'init'")
    print("3. python3 -m alembic upgrade head")
    
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    cur.close()
    conn.close()

