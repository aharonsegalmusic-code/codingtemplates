# CODEBASE SUMMARY
> One-line per project. Full details in DOCS.md.

---

## Templates & References

| Folder | Summary |
|--------|---------|
| `1.py_templates/` | Python code snippets: FastAPI+SQLAlchemy template, class patterns, error handling, file I/O, Pandas |
| `2.es_template/` | Elasticsearch learning project — pizza order data with 13+ query types (match, fuzzy, wildcard, range, aggregations) via FastAPI |
| `3.k8s/` | Bare Kubernetes YAML templates: app deployment + MySQL deployment, both with ClusterIP services |

---

## 4.k8s_fastapi_mongo — FastAPI + MongoDB + Kubernetes

| Folder | Summary |
|--------|---------|
| `4.k8s_fastapi_mongo/fastapi-k8s-mongo/` | Minimal FastAPI items API on MongoDB, with full production K8s manifests and deployment docs |
| `4.k8s_fastapi_mongo/week11_k8s_contacts/` | Contacts CRUD API on MongoDB + K8s; the best K8s learning docs in the repo (17 concepts explained) |
| `4.k8s_fastapi_mongo/week_11_k8_test/` | Single pod + service experiment — just testing that K8s can run a container |

---

## 5.mongodb_crud — MongoDB CRUD Exploration

| Folder | Summary |
|--------|---------|
| `5.mongodb_crud/` | Personal MongoDB CRUD exploration using employee JSON data; no real structure |

---

## 6.kafka_event_pipeline — Kafka + MongoDB + MySQL

| Folder | Summary |
|--------|---------|
| `6.kafka_event_pipeline/mongo/` | MongoDB query cheatsheet — all major query types (find, filter, sort, aggregate, lookup) as FastAPI routes |
| `6.kafka_event_pipeline/mini/` | Bare-minimum Kafka → MongoDB → MySQL pipeline; learning skeleton |
| `6.kafka_event_pipeline/week_17_kavka/` | Kafka producer/consumer pipeline: MongoDB as write DB, MySQL as analytics replica, separate analytics API, Kafka UI |
| `6.kafka_event_pipeline/kafka_mongo_sql_pipeline-main/` | Full CQRS e-commerce system — 5 entities (user, supplier, product, order, post), MongoDB → Kafka → MySQL sync, product state machine, 24 event types |

---

## 7.pizza_redis_pipeline — Redis + Multi-Stage Pipeline

| Folder | Summary |
|--------|---------|
| `7.pizza_redis_pipeline/week_18_redis/` | Redis intro: Kafka producer → consumer → MongoDB + Redis cache; analytics API reads cache-first |
| `7.pizza_redis_pipeline/sql-mondo-redis-kafka/` | Pizza order pipeline v1 — 5 services (API, text processor, kitchen, enricher, risk evaluator), BURNT/CANCELLED/DELIVERED states, Redis caching, Streamlit dashboard |
| `7.pizza_redis_pipeline/second-attempt/` | Pizza pipeline v2 — same flow as above but cleaner structure per service; adds Elasticsearch + Kibana |

---

## 8.elasticsearch_ocr_pipeline — Elasticsearch + OCR (Final Project)

| Folder | Summary |
|--------|---------|
| `8.elasticsearch_ocr_pipeline/` | OCR image pipeline — tweet images → pytesseract → Kafka → clean → Elasticsearch index + analytics; GridFS stores images; Streamlit dashboard searches ES and displays images |

---

## Learning Progression

```
4.k8s_fastapi_mongo          →   K8s + FastAPI + MongoDB
5.mongodb_crud               →   MongoDB deeper
6.kafka_event_pipeline       →   + Kafka + MySQL (event-driven sync, CQRS)
7.pizza_redis_pipeline       →   + Redis + multi-stage pipeline (pizza domain)
8.elasticsearch_ocr_pipeline →   + Elasticsearch + OCR + GridFS (capstone)
```

---

## Issues & Duplicates

| Issue | Detail |
|-------|--------|
| `7.pizza_redis_pipeline/sql-mondo-redis-kafka` ≈ `7.pizza_redis_pipeline/second-attempt` | Same pizza pipeline, same services — second-attempt is the improved rewrite |
| `7.pizza_redis_pipeline/second-attempt` ≈ `8.elasticsearch_ocr_pipeline` | Both: Kafka pipeline + ES + GridFS + Streamlit — week_19 adds OCR and is the final version |
| `6.kafka_event_pipeline/mini` ≈ `6.kafka_event_pipeline/week_17_kavka` | Both Kafka+MongoDB+MySQL — mini is the skeleton, kavka is the real thing |
| `4.k8s_fastapi_mongo/fastapi-k8s-mongo` ≈ `4.k8s_fastapi_mongo/week11_k8s_contacts` | Same stack, same architecture — items vs contacts |
| `5.mongodb_crud` | Minimal personal experiment, no proper documentation |
| `6.kafka_event_pipeline/mongo` | Not a deployable project — just a query reference file |
| `4.k8s_fastapi_mongo/week_11_k8_test` | Experiment only — not a real app |
