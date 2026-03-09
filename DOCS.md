# CODEBASE DOCUMENTATION
> Full searchable reference for all projects and sections.
> Tip: Use Ctrl+F to search for a technology, concept, or keyword.

---

## TABLE OF CONTENTS

| Folder | What it is |
|--------|-----------|
| [1.py_templates](#1py_templates) | Reusable Python & FastAPI code snippets |
| [2.es_template](#2es_template) | Elasticsearch learning project (pizza orders) |
| [3.k8s](#3k8s) | Standalone Kubernetes YAML reference |
| [4.k8s_fastapi_mongo/fastapi-k8s-mongo](#4k8s_fastapi_mongofastapi-k8s-mongo) | FastAPI + MongoDB deployed to Kubernetes |
| [4.k8s_fastapi_mongo/week11_k8s_contacts](#4k8s_fastapi_mongoweek11_k8s_contacts) | Contacts CRUD API + deep K8s docs |
| [4.k8s_fastapi_mongo/week_11_k8_test](#4k8s_fastapi_mongoweek_11_k8_test) | Minimal single-pod K8s experiment |
| [5.mongodb_crud](#5mongodb_crud) | MongoDB CRUD exploration |
| [6.kafka_event_pipeline/mongo](#6kafka_event_pipelinemongo) | MongoDB query patterns reference |
| [6.kafka_event_pipeline/mini](#6kafka_event_pipelinemini) | Minimal Kafka + MongoDB + MySQL pipeline |
| [6.kafka_event_pipeline/week_17_kavka](#6kafka_event_pipelineweek_17_kavka) | Kafka producer/consumer + analytics API |
| [6.kafka_event_pipeline/kafka_mongo_sql_pipeline-main](#6kafka_event_pipelinekafka_mongo_sql_pipeline-main) | Full CQRS e-commerce system |
| [7.pizza_redis_pipeline/week_18_redis](#7pizza_redis_pipelineweek_18_redis) | Redis introduction + basic pipeline |
| [7.pizza_redis_pipeline/sql-mondo-redis-kafka](#7pizza_redis_pipelinesql-mondo-redis-kafka) | Pizza order pipeline (first attempt) |
| [7.pizza_redis_pipeline/second-attempt](#7pizza_redis_pipelinesecond-attempt) | Pizza pipeline v2 + Elasticsearch |
| [8.elasticsearch_ocr_pipeline](#8elasticsearch_ocr_pipeline) | OCR image pipeline with ES + Kafka (final project) |

---
---

## 1.py_templates

**Path:** `1.py_templates/`
**What it is:** A collection of reusable Python templates and code patterns for common tasks.

### Files and what they contain

| File | Content |
|------|---------|
| `tem.md` | FastAPI + SQLAlchemy guide: models, schemas, CRUD, router wiring |
| `class.py` | Python class patterns (inheritance, dunder methods, properties) |
| `error_handeling.py` | Try/except patterns, custom exceptions, HTTP error raising |
| `file_handeling.py` | Reading, writing, appending files; CSV and JSON handling |
| `pd_template.py` | Pandas: DataFrame creation, filtering, groupby, merge, export |
| `html/basic_html.py` | Serving basic HTML from Python / FastAPI |

### fast_api/ — Complete FastAPI project template

| File | Content |
|------|---------|
| `main.py` | App entry point, lifespan, route registration |
| `database.py` | SQLAlchemy engine + session generator with `get_db()` |
| `models.py` (implied) | ORM table definitions |
| `schemas.py` | Pydantic request/response models with `from_attributes=True` |
| `router.py` | Route definitions using `APIRouter`, `Depends(get_db)` |

**Tech:** FastAPI, SQLAlchemy, Pydantic v2, SQLite
**Patterns:** Dependency injection, ORM mode, session-per-request

---
---

## 2.es_template

**Path:** `2.es_template/`
**What it is:** A complete Elasticsearch learning project. Models pizza order data to teach mappings, indexing, and all major query types through a FastAPI REST API.

### Files and what they contain

| File | Content |
|------|---------|
| `config.py` | ENV var loading (ES host, index name, etc.) |
| `es_client.py` | Elasticsearch client singleton (connection management) |
| `index_manager.py` | Create index with explicit mapping; bulk-load data from JSON |
| `queries.py` | All ES query implementations (see below) |
| `dal.py` | Data access layer — wraps query calls |
| `routes.py` | FastAPI route definitions |
| `main.py` | App entry point with lifespan (connects ES on startup) |
| `docker-compose.yml` | ES 8.13 + Kibana 8.13 + FastAPI |
| `K8S_GUIDE.md` | How to convert docker-compose → K8s with `kompose` |
| `KIBANA_GUIDE.md` | Kibana setup: index pattern, visualizations, dashboards |
| `es_exercise/` | 8 PDF exercise files (cat1–cat8) covering ES concepts |

### Query types implemented in `queries.py`

| Query | Method | ES type |
|-------|--------|---------|
| Get all orders | `get_all()` | `match_all` |
| Full-text search | `search_instructions()` | `match` |
| Multi-field search | `search_multi()` | `multi_match` |
| Typo-tolerant search | `search_fuzzy()` | `fuzzy` |
| Wildcard/glob search | `search_wildcard()` | `wildcard` |
| Exact match by type | `filter_by_type()` | `term` |
| Filter by delivery | `filter_by_delivery()` | `term` |
| Quantity range | `filter_quantity_range()` | `range` |
| Combined filters | `filter_delivery_by_type()` | `bool/must` |
| Count per pizza type | `count_by_type()` | `terms` aggregation |
| Quantity stats | `quantity_stats()` | `terms` aggregation |

### API Endpoints

```
GET  /                              Health check
GET  /orders/                       All orders
GET  /orders/{id}                   Single order
GET  /orders/search/instructions    Full-text search (q=)
GET  /orders/search/multi           Multi-field search (q=)
GET  /orders/search/fuzzy           Fuzzy search (q=)
GET  /orders/search/wildcard        Wildcard search (pattern=)
GET  /orders/filter/type            Filter by pizza type
GET  /orders/filter/delivery        Filter by is_delivery
GET  /orders/filter/quantity        Range filter (min_qty, max_qty)
GET  /orders/filter/delivery-by-type Combined filter
GET  /orders/agg/count-by-type      Aggregation: orders per type
GET  /orders/agg/quantity-by-type   Aggregation: quantity per type
```

**Tech:** FastAPI, Elasticsearch 8.13, Kibana, Docker Compose
**Index mapping:** Explicit field types — `text` + `keyword` sub-fields, `integer`, `boolean`
**Dev config:** Single shard, 0 replicas, security disabled

---
---

## 3.k8s

**Path:** `3.k8s/`
**What it is:** Standalone reference YAML manifests for a two-service app (web app + MySQL). Not a full project — just copy-paste templates.

### Files

| File | Content |
|------|---------|
| `app-deployment.yaml` | Deployment for application container |
| `app-service.yaml` | Service to expose the app (ClusterIP) |
| `mysql-deployment.yaml` | MySQL database deployment |
| `mysql-service.yaml` | ClusterIP service for MySQL (internal only) |

**Tech:** Kubernetes
**Use:** Reference for deployment + service pairing pattern

---
---

## 4.k8s_fastapi_mongo/fastapi-k8s-mongo

**Path:** `4.k8s_fastapi_mongo/fastapi-k8s-mongo/`
**What it is:** A minimal FastAPI app with MongoDB that is production-ready for Kubernetes. Includes full K8s manifests and documentation.

### Files and what they contain

| File | Content |
|------|---------|
| `app/main.py` | FastAPI with `GET /items` and `POST /items` |
| `app/database.py` | PyMongo connection using ENV vars |
| `app/crud.py` | Create and read item operations |
| `app/models.py` | Pydantic models for Item |
| `Dockerfile` | Python 3.11-slim + uvicorn |
| `docker-compose.yml` | FastAPI + MongoDB (local dev) |
| `.env` / `.env.compose` | `MONGO_URI`, `DB_NAME` config |
| `k8s/fastapi-deployment.yaml` | K8s Deployment for FastAPI |
| `k8s/fastapi-service.yaml` | LoadBalancer Service |
| `k8s/mongo-deployment.yaml` | K8s MongoDB deployment |
| `k8s/mongo-service.yaml` | ClusterIP service for Mongo |
| `docs/kubernetes.md` | K8s architecture concepts |
| `docs/mongo.md` | MongoDB setup guide |
| `docs/run.md` | Run instructions |
| `docs/k8_build.md` | Build + deploy steps |
| `docs/template.md` | Template explanation |

**Tech:** FastAPI, MongoDB 7, PyMongo, Docker, Kubernetes, Python 3.11
**Patterns:** ENV-driven config, service DNS resolution in K8s, PVC for MongoDB

---
---

## 4.k8s_fastapi_mongo/week11_k8s_contacts

**Path:** `4.k8s_fastapi_mongo/week11_k8s_contacts/`
**What it is:** Full contacts CRUD API with MongoDB, plus the most detailed Kubernetes educational documentation in the repo.

### App structure

| File | Content |
|------|---------|
| `app/main.py` | FastAPI app entry point |
| `app/routers/contacts.py` | Contacts CRUD routes |
| `app/routers/basic_test.py` | Health + DB test routes |
| `app/data/data_interactor.py` | Business logic layer |
| `app/data/db_use.py` | MongoDB operations |

### API Endpoints

```
GET    /test/health          Health check
GET    /test/db              DB connectivity test
GET    /contacts/            List all contacts
POST   /contacts/            Create contact
GET    /contacts/{id}        Get contact by ID
PUT    /contacts/{id}        Update contact
DELETE /contacts/{id}        Delete contact
```

### Documentation files

| File | Content |
|------|---------|
| `app/run.md` | How to run locally and in Docker |
| `kubernetes_flow.md` | Full K8s deploy workflow |
| `flow_test.md` | Step-by-step testing after deploy |
| `docs/kubernetes.md` | Glossary of 17 K8s concepts (Cluster, Node, Pod, Deployment, Service, ConfigMap, Secret, PV, PVC, Namespace, ReplicaSet, Ingress, VolumeMount, Labels, NodePort, ClusterIP, LoadBalancer) |
| `docs/mongo.md` | MongoDB on K8s |

### k8/ manifests

| File | Content |
|------|---------|
| `fastapi-deployment.yaml` | FastAPI deployment |
| `fastapi-service.yaml` | NodePort service |
| `fastapi-configmap.yaml` | ENV config map |
| `mongo-deployment.yaml` | MongoDB with PVC |
| `mongo-service.yaml` | ClusterIP for Mongo |

**Also includes `demo_app/`** — a simpler variant of the same app with `models/`, `routes/`, `services/`, `utils/` structure

**Tech:** FastAPI, MongoDB, PyMongo, Kubernetes, Docker
**Patterns:** ReadinessProbe, ConfigMap for ENV, PVC for persistent Mongo storage

---
---

## 4.k8s_fastapi_mongo/week_11_k8_test

**Path:** `4.k8s_fastapi_mongo/week_11_k8_test/`
**What it is:** Minimal single-service experiment for testing a pod and service in Kubernetes.

### Files

| File | Content |
|------|---------|
| `main.py` | Minimal FastAPI app |
| `Dockerfile` | Container image definition |
| `pod.yaml` | Raw K8s Pod manifest (no Deployment) |
| `service.yaml` | K8s Service manifest |
| `readme_pod_yaml.md` | Explanation of pod.yaml fields |
| `readme_service_yaml.md` | Explanation of service.yaml fields |
| `commands.txt` | kubectl commands used |
| `screenshot.png` | Screenshot of result |
| `requirements.txt` | Dependencies |

**Purpose:** Learning experiment — understanding the difference between Pod and Deployment, and how Service targets a Pod via labels.

---
---

## 5.mongodb_crud

**Path:** `5.mongodb_crud/`
**What it is:** MongoDB CRUD exploration project. Uses employee JSON data to practice MongoDB operations.

### Files

| File | Content |
|------|---------|
| `app/connection.py` | MongoDB connection setup |
| `app/dal.py` | Data access layer — CRUD operations |
| `app/main.py` | Entry point |
| `app/routs.py` | FastAPI routes |
| `app/json_to_mongo.py` | Load JSON data into MongoDB |
| `app/local_load.py` | Local data loading script |
| `employee_data_advanced.json` | Sample dataset (~88KB, employee records) |
| `requirements.txt` | Dependencies |

**Tech:** FastAPI, MongoDB, PyMongo
**Note:** Exploratory/personal project, minimal structure

---
---

## 6.kafka_event_pipeline/mongo

**Path:** `6.kafka_event_pipeline/mongo/`
**What it is:** MongoDB query patterns reference. A large collection of query examples organized by type.

### Files

| File | Content |
|------|---------|
| `mongo_db.py` | MongoDB connection setup |
| `mongo_insert.py` | Insert one, insert many, bulk write examples |
| `mongo_overview.py` | High-level overview of collections/stats |
| `query_main.py` | Large file (~14KB) with all query types: find, filter, sort, limit, skip, projection, aggregation pipeline, lookup (join), group, match, unwind |
| `routes_overview.py` | FastAPI route wrappers for overview queries |
| `routes_query_main.py` | FastAPI route wrappers for all query types |
| `main.py` | App entry, imports routes |

**Tech:** MongoDB, PyMongo, FastAPI
**Use:** Reference/cheatsheet for MongoDB query syntax

---
---

## 6.kafka_event_pipeline/mini

**Path:** `6.kafka_event_pipeline/mini/`
**What it is:** Stripped-down version of a Kafka + MongoDB + MySQL pipeline. Good for understanding the basic flow without the complexity of the full pipeline.

### Files

| File | Content |
|------|---------|
| `app/main.py` | FastAPI producer API |
| `app/models.py` | Data models |
| `consumer/main.py` | Kafka consumer |
| `consumer/models.py` | Consumer-side models |
| `ETL/main.py` | ETL pipeline script |
| `ETL/config.py` | DB config for ETL |
| `ETL/ddl.py` | MySQL table creation (DDL) |
| `data/users_with_posts.json` | Sample data |
| `docker-compose.yml` | MongoDB + MySQL + Kafka + app |
| `requirements.txt` | Dependencies |

**Tech:** Kafka, MongoDB 7, MySQL 8, FastAPI, Docker Compose
**Pattern:** Minimal producer → Kafka → consumer → MySQL

---
---

## 6.kafka_event_pipeline/week_17_kavka

**Path:** `6.kafka_event_pipeline/week_17_kavka/`
**What it is:** Kafka producer/consumer setup with MongoDB as the write DB and MySQL as the analytics DB. Includes a separate analytics query API.

### Services

| Service | Port | Description |
|---------|------|-------------|
| Producer (FastAPI) | varies | Accepts data, stores to MongoDB, publishes to Kafka |
| Consumer | — | Consumes from Kafka, writes to MySQL |
| Analytics API (FastAPI) | varies | Queries MySQL for analytics data |
| MongoDB | 27017 | Transactional storage |
| MySQL | 3307 | Analytics read replica |
| Kafka | 9092 | KRaft mode (no Zookeeper) |
| Kafka UI | 8001 | Web console for Kafka |

### Key files

| File | Content |
|------|---------|
| `producer/app/routes.py` | Ingest endpoints |
| `producer/app/kafka_publisher.py` | Kafka publish logic |
| `producer/app/mongo_connection.py` | MongoDB client |
| `consumer/app/kafka_consumer.py` | Kafka consume + dispatch |
| `consumer/app/mysql_connection.py` | MySQL connection |
| `consumer/app/sql_init.py` | MySQL schema init |
| `analytics-api/app/dal.py` | Analytics queries |
| `analytics-api/app/routes.py` | Analytics endpoints |
| `docker-compose.yml` | All services wired together |

**Tech:** Kafka 7.6.1 (KRaft), MongoDB 7, MySQL 8, FastAPI, Python
**Pattern:** Producer → Kafka → Consumer → MySQL; separate Analytics API reads MySQL

---
---

## 6.kafka_event_pipeline/kafka_mongo_sql_pipeline-main

**Path:** `6.kafka_event_pipeline/kafka_mongo_sql_pipeline-main/`
**What it is:** The most complete and complex project from week 17. A full CQRS-style e-commerce backend with 5 domain entities, event-driven sync between MongoDB and MySQL, state machines, and comprehensive task documentation.

### Architecture

```
FastAPI (mongo_backend) ──writes──► MongoDB
        │
        └──publishes──► Kafka (5 topics)
                              │
                        consumes──► mysql_server ──writes──► MySQL
```

### Domain entities

| Entity | MongoDB | Kafka topic | MySQL tables |
|--------|---------|-------------|--------------|
| User | ✓ | `user` | `users` |
| Supplier | ✓ | `supplier` | `suppliers` |
| Product | ✓ | `product` | `products`, `product_variants` |
| Order | ✓ | `order` | `orders`, `order_items` |
| Post | ✓ | `post` | `posts` |

### Key source files

| File | Content |
|------|---------|
| `shared/models/*.py` | Domain models shared between services |
| `shared/kafka/topics.py` | Kafka topic + event type constants |
| `apps/mongo_backend/services/*.py` | Business logic + event emission (one per entity) |
| `apps/mongo_backend/routes/*.py` | FastAPI route handlers |
| `apps/mongo_backend/schemas/*.py` | Pydantic request/response schemas |
| `apps/mongo_backend/kafka/producer.py` | Kafka publish logic |
| `apps/mysql_server/src/consumers/*.py` | Per-entity Kafka consumers |
| `apps/mysql_server/src/dal/*.py` | MySQL upsert/delete operations |
| `apps/mysql_server/src/db/tables.py` | MySQL schema (CREATE TABLE statements) |
| `apps/mysql_server/src/kafka/consumer.py` | Consumer dispatch loop |

### Product state machine

```
DRAFT ──publish──► ACTIVE ──discontinue──► DISCONTINUED
                     │
                     └──mark-out-of-stock──► OUT_OF_STOCK
```

### Event format (all topics)

```json
{
  "event_type": "user.created",
  "event_id": "<uuid4>",
  "timestamp": "<ISO-8601>",
  "entity_id": "<mongo-objectid>",
  "data": { ... }
}
```
Partition key = `entity_id` → ordered delivery per entity

### Task documentation (learning materials)

| File | Content |
|------|---------|
| `mongodb-tasks/TASK_01_USER.md` | Step-by-step MongoDB user implementation |
| `mongodb-tasks/TASK_02_SUPPLIER.md` | Supplier implementation |
| `mongodb-tasks/TASK_04_PRODUCT.md` | Product + state machine |
| `mongodb-tasks/TASK_05_POST.md` | Post + publish flow |
| `mongodb-tasks/TASK_07_ORDER.md` | Order + OrderItem |
| `mongodb-tasks/TASK_08_ANALYTICS.md` | Analytics queries |
| `mongodb-tasks/TASK_09_KAFKA.md` | Kafka integration |
| `mysql-tasks/TASK_0*.md` | MySQL equivalents for each entity |
| `ARCHITECTURE.md` | Full system architecture doc |

**Tech:** FastAPI, MongoDB (Beanie ODM), MySQL 8, Kafka 7.6 (KRaft), Docker Compose
**Patterns:** CQRS, event sourcing, denormalization (ProductSnapshot, PostAuthor), soft deletes (`deleted_at`), Beanie ODM, state machines

---
---

## 7.pizza_redis_pipeline/week_18_redis

**Path:** `7.pizza_redis_pipeline/week_18_redis/`
**What it is:** Redis introduction project. A Kafka producer/consumer pipeline that adds Redis caching and a MongoDB-backed analytics API.

### Services

| Service | Port | Description |
|---------|------|-------------|
| Producer (FastAPI) | varies | Generates/receives data, publishes to Kafka |
| Consumer | — | Kafka consumer, writes to MongoDB + Redis |
| Analytics API (FastAPI) | varies | Reads from MongoDB + Redis cache |
| MongoDB | 27017 | Persistent storage |
| Redis | 6379 | Cache layer |
| Kafka | 9092 | Message broker |

### Key files

| File | Content |
|------|---------|
| `producer/main.py` | Producer logic |
| `producer/redis_connection.py` | Redis client setup |
| `producer/priority_logic.py` | Priority/classification logic |
| `producer/border_alerts.json` | Sample domain data |
| `consumer/main.py` | Kafka consume + MongoDB write |
| `consumer/redis_connection.py` | Redis client |
| `consumer/mongo_connection.py` | MongoDB client |
| `analytics-api/dal.py` | Data queries (MongoDB + Redis) |
| `analytics-api/routes.py` | API endpoints |
| `analytics-api/redis_connection.py` | Redis reads |
| `docker-compose.yml` | All services |
| `plans.md` | Design plan notes |

**Tech:** Kafka, MongoDB, Redis 7, FastAPI, Docker
**Pattern:** Producer → Kafka → Consumer → MongoDB/Redis; Analytics API reads cache-first

---
---

## 7.pizza_redis_pipeline/sql-mondo-redis-kafka

**Path:** `7.pizza_redis_pipeline/sql-mondo-redis-kafka/redis_start/`
**What it is:** First-attempt pizza order processing pipeline. Multi-service system where orders pass through cleaning, enrichment, kitchen simulation, and risk evaluation stages.

### System flow

```
Client → API :8000 → MongoDB + Kafka (pizza_orders)
                              ↓              ↓
                     Text Processor     Kitchen Worker
                     (clean text,       (simulate 15s cook,
                      allergy check)     mark DELIVERED)
                              ↓
                     Kafka (cleaned-instructions)
                              ↓
                          Enricher
                     (kosher analysis:
                      meat+dairy = BURNT)
                              ↓ (every 10s poll)
                     Risk Evaluator
                     (allergen match → CANCELLED)
                              ↓
                     Redis (cache metrics, 30s TTL)
                              ↓
                     Dashboard :8501 (Streamlit)
```

### Order status transitions

| Transition | Triggered by |
|------------|-------------|
| → DELIVERING | Kitchen worker (after 15s) |
| → BURNT | Enricher (meat + dairy ingredients) |
| → CANCELLED | Risk evaluator (allergen match — overrides all) |

### Services and key files

| Service | File | Content |
|---------|------|---------|
| API | `api/api.py` | Upload JSON orders, query status |
| API | `api/router.py` | Route definitions |
| API | `api/connection/*.py` | Kafka, Mongo, MySQL, Redis clients |
| Text Processor | `text_processor/text_worker.py` | Kafka consumer, clean + check text |
| Text Processor | `text_processor/clean_preprocessor.py` | Cleaning + allergy logic |
| Kitchen | `kitchen/kitchen_worker.py` | Kafka consumer, 15s timer, DELIVERED |
| Enricher | `enricher/enricher_consumer.py` | Kosher analysis, BURNT logic |
| All | `*/connection/*.py` | Per-service DB/Kafka clients |
| Data | (in api) | `pizza_orders.json`, `pizza_prep.json`, `pizza_analysis_lists.json` |
| Dashboard | Streamlit | Real-time order/allergen visualization |
| `docker-compose.yml` | — | MongoDB, MySQL, Kafka, Redis, CloudBeaver, RedisInsight, Kafka UI, Streamlit |
| `STATE.MD` | — | Current project state |

**Tech:** FastAPI, Kafka (KRaft), MongoDB 7, MySQL 8, Redis 7, Pandas, Streamlit, Docker
**Analysis lists:** `forbidden_non_kosher`, `meat_ingredients`, `dairy_ingredients`, `common_allergens`

---
---

## 7.pizza_redis_pipeline/second-attempt

**Path:** `7.pizza_redis_pipeline/second-attempt/`
**What it is:** Refined version of the pizza pipeline with a cleaner architecture, better separation per service, and Elasticsearch added for searchability. More production-like structure.

> **Note:** Same domain and same services as `sql-mondo-redis-kafka` but better organized and adds Elasticsearch + Kibana.

### Services

| Service | Port | Description |
|---------|------|-------------|
| API | 8000 | Ingest orders, publish to Kafka |
| Text Processor | — | Kafka consumer: clean + preprocess |
| Kitchen Worker | — | Kafka consumer: cooking simulation |
| Enricher | — | Kafka consumer: kosher + allergen analysis |
| Risk Evaluator | — | Polls MongoDB every 10s, allergen check |
| Dashboard | 8501 | Streamlit visualization |
| MongoDB | 27017 | Order storage |
| Kafka | 9092 | KRaft message broker |
| Redis | 6379 | Metrics caching |

### Key files

| File | Content |
|------|---------|
| `api/api.py` | Main FastAPI app |
| `api/router.py` | Route definitions |
| `api/connection/*.py` | Kafka producer, Mongo, MySQL, Redis clients |
| `text_processor/text_worker.py` | Kafka consume + dispatch |
| `text_processor/clean_preprocessor.py` | Text cleaning logic |
| `enricher/enricher_consumer.py` | Kosher/allergen analysis |
| `kitchen/kitchen_worker.py` | Cooking simulation |
| `risk_evaluator/risk_evaluator.py` | Pandas-based allergen matching |
| `dashboard/dashboard.py` | Streamlit UI |
| `dashboard/connection/*.py` | Mongo + Redis clients for dashboard |
| `docker-compose.yml` | 9 containers |
| `project_dump.md` | Full project documentation |
| `STATE.MD` | Implementation state |

**Tech:** FastAPI, Kafka (KRaft), MongoDB 7, Redis, Pandas, Streamlit, Docker
**Patterns:** Each service has its own `connection/` folder; risk evaluator uses Pandas DataFrames for batch allergen matching

---
---

## 8.elasticsearch_ocr_pipeline

**Path:** `8.elasticsearch_ocr_pipeline/`
**What it is:** The final and most complete project. An OCR-based image ingestion pipeline that extracts text from tweet images, cleans it, indexes it into Elasticsearch, and provides a search dashboard. Combines all previous technologies.

### Architecture

```
Images (PNG) → Ingestion API :8000
                    ↓ (OCR with pytesseract)
                MongoDB (raw doc + GridFS for images)
                    ↓ (publish)
              Kafka: raw_images
                    ↓
          Cleaning Consumer
          (stop words, normalize)
                    ↓ (publish)
              Kafka: cleaned_text
                    ↓↓ (two consumers)
        ┌──────────┴──────────┐
Elastic Consumer          Analytics Consumer
(index to ES)             (compute stats)
        ↓                         ↓
 Elasticsearch             Kafka: analytics
 (searchable index)               ↓
        ↓                  Analytics service
 GridFS Service API :8001         ↓
 (serve images)           MongoDB (store results)
        ↓
  Dashboard (Streamlit)
  → search ES, show images from GridFS
```

### Services and key files

| Service | Key files | Description |
|---------|-----------|-------------|
| `ingestion_service_api/` | `OCRengine.py`, `ingestion_orchestrator.py`, `routes.py`, `mongo_client.py`, `metadata_extractor.py` | Upload images → OCR → MongoDB + Kafka |
| `cleaning_consumer/` | `text_cleaner.py`, `clean_orchestrator.py`, `clean_config.py` | Consume raw → clean text → re-publish |
| `elastic_consumer/` | `kafkaConsumer.py`, `indexOrchestrator.py`, `indexerConfig.py` | Consume cleaned → index to ES |
| `analytics/` | `textAnalyzer.py`, `analyticsOrchestrator.py`, `kafkaConsumer.py`, `kafkaPublisher.py` | Analyze text, compute stats, publish results |
| `GridFS_service_api/` | `GridFSStorage.py`, `GridFsOrchestrator.py`, `GridFSConfig.py`, `routes.py` | Store/serve images via MongoDB GridFS |
| `dashboard/` | `dashboard.py`, `searchService.py`, `routes.py`, `connection/*.py` | Streamlit: search ES, display images |
| `shared/` | `es_connection.py`, `kafka_consumer.py`, `kafka_publisher.py`, `mongo_connection.py`, `logger.py`, `image_model.py` | Shared utilities across all services |

### Shared utilities (`shared/`)

| File | Content |
|------|---------|
| `es_connection.py` | Elasticsearch client singleton |
| `mongo_connection.py` | MongoDB client singleton |
| `kafka_consumer.py` | Base Kafka consumer class |
| `kafka_publisher.py` | Base Kafka publisher class |
| `image_model.py` | Pydantic model for image document |
| `logger.py` | Centralized logging setup |

### Kafka topics

| Topic | Published by | Consumed by |
|-------|-------------|-------------|
| `raw_images` | Ingestion API | Cleaning Consumer |
| `cleaned_text` | Cleaning Consumer | Elastic Consumer, Analytics |
| `analytics` | Analytics | (stored to MongoDB) |

### Other files

| File | Content |
|------|---------|
| `docker-compose.yml` | 14 containers: all services + MongoDB + Kafka + ES + Kibana + Redis |
| `requirements.txt` | All Python deps (pytesseract, elasticsearch, confluent-kafka, etc.) |
| `project_dump.md` | ~81KB comprehensive project documentation |
| `rules_claude.md` | Implementation rules/constraints |
| `discuss.md` | Design discussion notes |
| `tests/` | Unit tests for OCR, consumer, stop words |
| `ingestion_service_api/images/` | Sample tweet images (tweet_0.png, tweet_1.png, tweet_2.png) |

**Tech:** FastAPI, Kafka (KRaft), MongoDB 7, Elasticsearch 8, Kibana, Redis, GridFS, Streamlit, pytesseract (OCR), Docker Compose
**Patterns:** Shared connection singletons, base Kafka classes, centralized logging, GridFS for binary storage, ES for full-text search

---
---

## ISSUES, DUPLICATES & NOTES

### Duplicates / Overlap

| Projects | Overlap |
|----------|---------|
| `7.pizza_redis_pipeline/sql-mondo-redis-kafka` ↔ `7.pizza_redis_pipeline/second-attempt` | Same domain (pizza orders), same services. `second-attempt` is the improved rewrite. |
| `7.pizza_redis_pipeline/second-attempt` ↔ `8.elasticsearch_ocr_pipeline` | Both are multi-stage Kafka pipelines with ES, cleaning, analytics, GridFS, and Streamlit. `8.elasticsearch_ocr_pipeline` is the final evolved version with OCR added. |
| `6.kafka_event_pipeline/mini` ↔ `6.kafka_event_pipeline/week_17_kavka` | Both are Kafka + MongoDB + MySQL pipelines. `mini` is the stripped-down learning version; `week_17_kavka` is the proper implementation. |
| `4.k8s_fastapi_mongo/fastapi-k8s-mongo` ↔ `4.k8s_fastapi_mongo/week11_k8s_contacts` | Both FastAPI + MongoDB + K8s. Same architecture, different data (items vs contacts). |

### Learning Progression

```
4.k8s_fastapi_mongo          →  K8s + FastAPI + MongoDB
5.mongodb_crud               →  MongoDB deeper dive
6.kafka_event_pipeline       →  + Kafka (producer/consumer) + MySQL
7.pizza_redis_pipeline       →  + Redis caching + multi-stage pipeline (pizza domain)
8.elasticsearch_ocr_pipeline →  + Elasticsearch + OCR + GridFS (final capstone)
```

### Minor notes

- `5.mongodb_crud` is a purely personal exploration project, minimal structure
- `6.kafka_event_pipeline/mongo` is a query reference/cheatsheet, not a deployable project
- `3.k8s/` at root is a standalone reference, not tied to any specific project
- `4.k8s_fastapi_mongo/week_11_k8_test` is a minimal experiment — just a pod + service test, not a full app
- `2.es_template` has a dedicated `es_exercise/` folder with 8 PDF category exercises (cat1–cat8) covering ES from setup through nested fields
