# Week 17 — Kafka + Multi-Database Event Pipeline

Introduction to event-driven architecture with Kafka. Projects progress from a basic query reference up to a full CQRS e-commerce system.

---

## Sub-projects

- `mongo/` — MongoDB query patterns cheatsheet (not a deployable app — just reference code)
- `mini/` — Bare-minimum Kafka → MongoDB → MySQL pipeline; learning skeleton
- `week_17_kavka/` — Kafka producer/consumer with MongoDB as write DB, MySQL as analytics replica, and a separate analytics query API
- `kafka_mongo_sql_pipeline-main/` — Full CQRS e-commerce system: 5 domain entities, MongoDB → Kafka → MySQL sync, product state machine, 24 event types

## Key concepts covered

- Kafka KRaft mode (no Zookeeper)
- Kafka producer / consumer patterns
- Event-driven sync between MongoDB (writes) and MySQL (analytics reads)
- CQRS: separate write and read databases
- Beanie ODM for MongoDB
- State machines (product lifecycle)
- Denormalized snapshots (ProductSnapshot, PostAuthor)
- Soft deletes with `deleted_at`
