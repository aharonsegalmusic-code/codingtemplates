# redis_test.py
#
# Goal
# - connect to Redis
# - write a few keys (string, hash, list) so you can SEE them in RedisInsight UI
# - read them back and print results
#
# Reads configuration ONLY from an env file (NOT from OS environment)
#
# install:
#   pip install redis python-dotenv
#
# env files:
#   .env.local  (host-run)  REDIS_HOST=127.0.0.1 ...
#   .env.prod   (prod)      REDIS_HOST=...         ...
#
# required env vars:
#   REDIS_HOST
#   REDIS_PORT
#   REDIS_PASSWORD  (can be empty)
#   REDISINSIGHT_URL (optional, just printed)
#
# usage:
#   python redis_test.py

from __future__ import annotations

import json
import time
import uuid
from datetime import datetime, timezone

import redis
from dotenv import dotenv_values

# =========================================================
# ENV FILE MODE (change this)
# =========================================================
PRODUCTION = False  # False -> .env.local, True -> .env.prod

ENV_PATH = ".env.prod" if PRODUCTION else ".env.local"
ENV = dotenv_values(ENV_PATH)  # NOTE: reads ONLY from the file, does NOT use os.environ


def must_get(key: str) -> str:
    v = ENV.get(key)
    if v is None or str(v).strip() == "":
        raise RuntimeError(f"Missing required key in {ENV_PATH}: {key}")
    return str(v)


REDIS_HOST = must_get("REDIS_HOST")
REDIS_PORT = int(must_get("REDIS_PORT"))
REDIS_PASSWORD = str(ENV.get("REDIS_PASSWORD", "") or "")
REDISINSIGHT_URL = str(ENV.get("REDISINSIGHT_URL", "") or "")

# keep the keys grouped so it's easy to find in UI
KEY_PREFIX = "test:redis"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def main():
    run_id = uuid.uuid4().hex

    print("redis settings:")
    print(f"  host={REDIS_HOST}")
    print(f"  port={REDIS_PORT}")
    print(f"  password_set={'YES' if REDIS_PASSWORD else 'NO'}")
    if REDISINSIGHT_URL:
        print(f"  ui={REDISINSIGHT_URL}")

    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD if REDIS_PASSWORD else None,
        decode_responses=True,
        socket_connect_timeout=3,
        socket_timeout=3,
    )

    # TEST CONNECT
    pong = r.ping()
    print(f"TEST CONNECT: ping -> {pong}")

    # Keys we will create (TTL so they auto-clean)
    ttl_seconds = 600  # 10 minutes

    key_str = f"{KEY_PREFIX}:string:{run_id}"
    key_hash = f"{KEY_PREFIX}:hash:{run_id}"
    key_list = f"{KEY_PREFIX}:list:{run_id}"

    # ---------------------------
    # WRITE
    # ---------------------------
    print("TEST REDIS WRITE: creating keys...")

    # STRING
    payload = {"type": "redis_test", "run_id": run_id, "ts": now_iso(), "msg": "hello redis"}
    r.set(key_str, json.dumps(payload, ensure_ascii=False))
    r.expire(key_str, ttl_seconds)

    # HASH
    r.hset(
        key_hash,
        mapping={
            "type": "redis_test",
            "run_id": run_id,
            "ts": now_iso(),
            "n": "1",
        },
    )
    r.expire(key_hash, ttl_seconds)

    # LIST
    r.rpush(key_list, "a", "b", "c")
    r.expire(key_list, ttl_seconds)

    print(f"TEST REDIS WRITE: OK (ttl={ttl_seconds}s)")
    print("  created:")
    print("   ", key_str)
    print("   ", key_hash)
    print("   ", key_list)

    # ---------------------------
    # READ BACK
    # ---------------------------
    print("\nTEST REDIS READ: reading keys back...")

    got_str = r.get(key_str)
    got_hash = r.hgetall(key_hash)
    got_list = r.lrange(key_list, 0, -1)

    print("STRING get ->", got_str)
    print("HASH hgetall ->", got_hash)
    print("LIST lrange ->", got_list)

    # quick assertions
    if got_str is None or run_id not in got_str:
        raise SystemExit("FAIL: string value not found / mismatch")
    if got_hash.get("run_id") != run_id:
        raise SystemExit("FAIL: hash value not found / mismatch")
    if got_list != ["a", "b", "c"]:
        raise SystemExit("FAIL: list value mismatch")

    print("\nOK redis_test completed")

    # Helpful UI instructions
    print("\nTo see it in RedisInsight:")
    if REDISINSIGHT_URL:
        print(f"  1) open {REDISINSIGHT_URL}")
    else:
        print("  1) open RedisInsight (your mapped port, usually http://127.0.0.1:5540)")

    print("  2) search keys with prefix:", KEY_PREFIX)
    print("  3) you should see 3 keys with this run_id:", run_id)
    print("NOTE: keys expire automatically in 10 minutes (ttl).")


if __name__ == "__main__":
    main()