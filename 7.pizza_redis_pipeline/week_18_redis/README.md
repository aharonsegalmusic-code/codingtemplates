# Redis Introduction — Kafka + MongoDB + Redis Cache

First project using Redis. A Kafka pipeline where the consumer writes to both MongoDB (persistent) and Redis (cache), and an analytics API reads from Redis first for speed.

---

## Services

- `producer/` — FastAPI API: generates/receives data, applies priority logic, publishes to Kafka
- `consumer/` — Kafka consumer: writes to MongoDB and updates Redis cache
- `analytics-api/` — FastAPI: reads from Redis cache first, falls back to MongoDB

## What's here

- `producer/main.py` — Producer logic and endpoints
- `producer/priority_logic.py` — Priority/classification rules
- `producer/redis_connection.py` — Redis client setup
- `producer/border_alerts.json` — Sample domain data
- `consumer/main.py` — Kafka consume + MongoDB write + Redis update
- `consumer/redis_connection.py` — Redis client
- `consumer/mongo_connection.py` — MongoDB client
- `analytics-api/dal.py` — Data queries (Redis first, MongoDB fallback)
- `analytics-api/routes.py` — API endpoints
- `analytics-api/redis_connection.py` — Redis reads
- `docker-compose.yml` — All services wired together
- `plans.md` — Design notes

**Stack:** Kafka · MongoDB · Redis 7 · FastAPI · Docker Compose
