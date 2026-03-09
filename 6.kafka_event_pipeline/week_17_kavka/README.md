# Kafka Producer/Consumer with MongoDB + MySQL Analytics

A complete Kafka pipeline: data comes in through a FastAPI producer, gets stored in MongoDB and published to Kafka, consumed into MySQL, and queried through a separate analytics API.

---

## Services

- `producer/` — FastAPI API: accepts data, stores to MongoDB, publishes to Kafka
- `consumer/` — Kafka consumer: reads events, writes to MySQL
- `analytics-api/` — FastAPI API: reads from MySQL for analytics queries

## What's here

- `producer/app/routes.py` — Ingest endpoints
- `producer/app/kafka_publisher.py` — Kafka publish logic
- `producer/app/mongo_connection.py` — MongoDB client
- `consumer/app/kafka_consumer.py` — Kafka consume + dispatch
- `consumer/app/mysql_connection.py` — MySQL connection
- `consumer/app/sql_init.py` — MySQL schema initialization
- `analytics-api/app/dal.py` — Analytics queries against MySQL
- `analytics-api/app/routes.py` — Analytics API endpoints
- `docker-compose.yml` — MongoDB + MySQL + Kafka (KRaft) + Kafka UI + all services

## Run

```bash
docker compose up --build
docker compose logs --tail=200 producer
docker compose logs --tail=200 consumer
docker compose logs --tail=200 analytics-api
docker compose down -v
```

**Stack:** Kafka 7.6.1 (KRaft) · MongoDB 7 · MySQL 8 · FastAPI · Kafka UI
