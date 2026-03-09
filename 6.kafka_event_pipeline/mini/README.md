# Kafka + MongoDB + MySQL Mini Pipeline

Stripped-down learning skeleton for a Kafka-based pipeline. Covers the basic flow without the complexity of the full pipeline.

---

## What's here

- `app/main.py` — FastAPI producer API
- `app/models.py` — Data models
- `consumer/main.py` — Kafka consumer (reads from topic, writes to MySQL)
- `consumer/models.py` — Consumer-side models
- `ETL/main.py` — ETL pipeline script
- `ETL/config.py` — DB config for ETL
- `ETL/ddl.py` — MySQL table creation (DDL statements)
- `data/users_with_posts.json` — Sample data
- `docker-compose.yml` — MongoDB + MySQL + Kafka + app
- `requirements.txt` — Python dependencies

**Flow:** FastAPI → Kafka topic → Consumer → MySQL

**Stack:** Kafka · MongoDB 7 · MySQL 8 · FastAPI · Docker Compose
