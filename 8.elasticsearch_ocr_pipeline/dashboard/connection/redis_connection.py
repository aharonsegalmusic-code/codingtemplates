import os
from dotenv import dotenv_values
import redis

ENV = {**dotenv_values(".env.local"), **os.environ}

REDIS_HOST = ENV.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(ENV.get("REDIS_PORT", "6379"))
REDIS_PASSWORD = ENV.get("REDIS_PASSWORD", "") or None

def get_redis_client() -> redis.Redis:
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True,
    )

r = get_redis_client()
