from redis.asyncio.client import Redis, ConnectionError

# Create Redis connection client
async def redis_client() -> Redis:
    try:
        return await Redis.from_url(
            f"redis://redis:6379/0",
            encoding="utf8", 
            decode_responses=True
        )
    except ConnectionError as e:
        print("Connection error:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)