# Week 18 — Redis + Multi-Stage Processing Pipeline

Adds Redis caching to the stack and introduces multi-stage event processing pipelines. The domain is pizza orders passing through multiple processing stages. Three projects at increasing levels of refinement.

---

## Sub-projects

- `week_18_redis/` — Redis introduction: Kafka producer/consumer pipeline with MongoDB storage and Redis cache; separate analytics API reads cache-first
- `sql-mondo-redis-kafka/` — Pizza order pipeline v1: 5 processing services (API, text processor, kitchen, enricher, risk evaluator), BURNT/CANCELLED/DELIVERED status machine, Streamlit dashboard
- `second-attempt/` — Pizza pipeline v2: same flow, cleaner per-service structure, adds Elasticsearch + Kibana

## Key concepts covered

- Redis caching with TTL
- Multi-stage Kafka pipelines (order flows through multiple consumers)
- Order status state machines with override rules (CANCELLED beats all)
- Pandas DataFrames for batch allergen analysis
- Streamlit real-time dashboard
- Closed-list analysis (allergens, kosher rules, meat/dairy detection)
- Per-service `connection/` isolation pattern
