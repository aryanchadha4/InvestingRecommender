# Redis Setup Guide

## Quick Start

### Option 1: Install Redis with Homebrew (Recommended for macOS)

```bash
# Install Redis
brew install redis

# Start Redis (runs in background)
brew services start redis

# Or run Redis manually in foreground
redis-server
```

**Verify:**
```bash
redis-cli ping
# Should return: PONG
```

### Option 2: Use Docker

```bash
# Start Redis container
docker run -d -p 6379:6379 --name redis redis:7

# Check if running
docker ps | grep redis

# Stop Redis
docker stop redis

# Start existing container
docker start redis
```

### Option 3: Use the Helper Script

```bash
./start_redis.sh
```

## Troubleshooting

**Redis not starting:**
- Check if port 6379 is already in use: `lsof -i :6379`
- Kill existing Redis: `pkill redis-server`
- Restart: `brew services restart redis`

**Connection refused:**
- Verify Redis is running: `redis-cli ping`
- Check Redis is listening on correct port: `lsof -i :6379`
- Verify REDIS_URL in environment: `echo $REDIS_URL`

**Docker issues:**
- Check Docker is running: `docker ps`
- Remove old container: `docker rm -f redis`
- Start fresh: `docker run -d -p 6379:6379 --name redis redis:7`
