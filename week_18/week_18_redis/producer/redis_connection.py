import redis
from dotenv import dotenv_values

config = dotenv_values(".env")

REDIS_HOST = config.get("REDIS_HOST", "redis")
REDIS_PORT = int(config.get("REDIS_PORT", "6379"))


def get_redis_client():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True,
    )


r = get_redis_client()

