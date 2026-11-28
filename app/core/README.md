
Option 1: Install Redis using Homebrew (recommended)
Open your terminal:

1. Install Redis


bash
brew install redis
2. Start Redis


bash
brew services start redis
3. Check Redis status


bash
brew services info redis
4. Test connection


bash
redis-cli ping
Expected response:


text
PONG
Redis running
Your FastAPI application should now be able to connect.

Option 2: Run Redis using Docker
If you prefer Docker:


bash
docker run -d \
  --name local-redis \
  -p 6379:6379 \
  redis:7-alpine
Test:


bash
docker exec -it local-redis redis-cli ping
Expected:


text
PONG
To stop Redis:


bash
docker stop local-redis

To start it again:


bash
docker start local-redis