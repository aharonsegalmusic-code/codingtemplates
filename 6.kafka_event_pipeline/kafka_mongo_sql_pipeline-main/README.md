# CQRS E-Commerce Pipeline — MongoDB + Kafka + MySQL

The most complete project from week 17. A full event-driven e-commerce backend with 5 domain entities, MongoDB as the write database, MySQL as the analytics read replica, and Kafka syncing them in real time.

---

## Architecture

```
FastAPI (mongo_backend) → writes → MongoDB
         └── publishes → Kafka (5 topics)
                              └── consumes → mysql_server → MySQL
```

## Domain entities

| Entity | Kafka topic | MySQL tables |
|--------|-------------|--------------|
| User | `user` | `users` |
| Supplier | `supplier` | `suppliers` |
| Product | `product` | `products`, `product_variants` |
| Order | `order` | `orders`, `order_items` |
| Post | `post` | `posts` |

## Product state machine

```
DRAFT → ACTIVE → DISCONTINUED
          └→ OUT_OF_STOCK
```

## What's here

- `shared/models/` — Domain models shared between both services
- `shared/kafka/topics.py` — Kafka topic + event type constants (24 event types)
- `apps/mongo_backend/services/` — Business logic + Kafka event emission (one file per entity)
- `apps/mongo_backend/routes/` — FastAPI route handlers
- `apps/mongo_backend/schemas/` — Pydantic request/response schemas
- `apps/mongo_backend/kafka/producer.py` — Kafka publish logic
- `apps/mysql_server/src/consumers/` — Per-entity Kafka consumers
- `apps/mysql_server/src/dal/` — MySQL upsert/delete operations
- `apps/mysql_server/src/db/tables.py` — MySQL schema (CREATE TABLE statements)
- `mongodb-tasks/` — Step-by-step implementation task docs (TASK_01 through TASK_09)
- `mysql-tasks/` — MySQL equivalent task docs
- `ARCHITECTURE.md` — Full system architecture documentation
- `docker-compose.yml` — MongoDB + Kafka + FastAPI + MySQL + mysql_server

## Key patterns

- CQRS: MongoDB for writes, MySQL for analytics reads
- Denormalized snapshots: `ProductSnapshot`, `PostAuthor` (immutable references)
- Soft deletes via `deleted_at` timestamp
- Beanie ODM for MongoDB document handling
- Partition key = `entity_id` → ordered Kafka delivery per entity

**Stack:** FastAPI · MongoDB (Beanie ODM) · MySQL 8 · Kafka 7.6 (KRaft) · Docker Compose
