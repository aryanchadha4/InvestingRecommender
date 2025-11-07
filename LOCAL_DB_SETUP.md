# Local PostgreSQL Database Setup (Without Docker)

## Step 1: Install PostgreSQL

### Option A: Using Homebrew (Recommended)

1. **Accept Xcode license** (if needed):
   ```bash
   sudo xcodebuild -license accept
   ```

2. **Install PostgreSQL:**
   ```bash
   brew install postgresql@16
   ```

3. **Start PostgreSQL service:**
   ```bash
   brew services start postgresql@16
   ```

### Option B: Using Postgres.app (Easier GUI Option)

1. **Download Postgres.app:**
   - Visit: https://postgresapp.com/
   - Download and install the .dmg file
   - Open Postgres.app from Applications
   - Click "Initialize" to create a new server

2. **Add to PATH** (optional, for command line access):
   ```bash
   echo 'export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

## Step 2: Create Database and User

### Using psql (Command Line)

```bash
# Connect to PostgreSQL (default user is usually your macOS username)
psql postgres

# Then run these SQL commands:
CREATE USER invest WITH PASSWORD 'invest';
CREATE DATABASE investdb OWNER invest;
GRANT ALL PRIVILEGES ON DATABASE investdb TO invest;

# Exit psql
\q
```

### Using Postgres.app

1. Open Postgres.app
2. Click "Open psql" or use the terminal
3. Run the same SQL commands as above

## Step 3: Update Environment File

Update your `.env` file to use `localhost` instead of `db`:

```bash
DATABASE_URL=postgresql+psycopg://invest:invest@localhost:5432/investdb
REDIS_URL=redis://localhost:6379/0
ENV=dev
SECRET_KEY=change-me
```

## Step 4: Verify Connection

Test the connection:
```bash
cd backend
python3 -c "from app.core.config import settings; print('Database URL:', settings.database_url)"
```

## Step 5: Run Migrations

Once the database is set up:
```bash
cd backend
python3 -m alembic revision --autogenerate -m "init"
python3 -m alembic upgrade head
```

## Troubleshooting

**Port 5432 already in use:**
- Check what's using it: `lsof -i :5432`
- Stop other PostgreSQL instances or change the port

**Connection refused:**
- Make sure PostgreSQL is running: `brew services list` (if using Homebrew)
- Check Postgres.app is running (if using Postgres.app)

**psql: command not found:**
- Add PostgreSQL to PATH (see Postgres.app instructions above)
- Or use full path: `/Applications/Postgres.app/Contents/Versions/latest/bin/psql`

