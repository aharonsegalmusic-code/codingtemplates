# Tweet OCR Pipeline — Elasticsearch + Kafka + MongoDB + GridFS

Final capstone project. Ingests tweet images, extracts text via OCR, cleans it, indexes it into Elasticsearch, computes analytics, and serves a searchable dashboard. Combines every technology from the learning journey.

---

## Architecture

```
Images → Ingestion API :8000
              ↓ OCR (pytesseract)
         MongoDB + GridFS (raw storage)
              ↓ publish
         Kafka: raw_images
              ↓
       Cleaning Consumer
       (stop words, normalize)
              ↓ publish
         Kafka: cleaned_text
              ↓               ↓
   Elastic Consumer     Analytics Consumer
   → Elasticsearch      → Kafka: analytics
     (searchable)         → MongoDB (stats)
              ↓
       GridFS Service :8001
       (serve images by ID)
              ↓
       Streamlit Dashboard
       (search ES, display images)
```

## Services

- `ingestion_service_api/` — Upload images, run OCR, store to MongoDB + GridFS, publish to Kafka
- `cleaning_consumer/` — Consume raw text, clean (stop words, normalize), re-publish
- `elastic_consumer/` — Consume cleaned text, index documents into Elasticsearch
- `analytics/` — Consume cleaned text, compute stats, publish analytics events
- `GridFS_service_api/` — Store and serve binary image files via MongoDB GridFS
- `dashboard/` — Streamlit UI: search Elasticsearch, display images from GridFS
- `shared/` — Shared utilities used by all services

## What's in shared/

- `es_connection.py` — Elasticsearch client singleton
- `mongo_connection.py` — MongoDB client singleton
- `kafka_consumer.py` — Base Kafka consumer class
- `kafka_publisher.py` — Base Kafka publisher class
- `image_model.py` — Pydantic model for image documents
- `logger.py` — Centralized logging setup

## Kafka topics

| Topic | From | To |
|-------|------|----|
| `raw_images` | Ingestion API | Cleaning Consumer |
| `cleaned_text` | Cleaning Consumer | Elastic Consumer, Analytics |
| `analytics` | Analytics | MongoDB storage |

## Other files

- `docker-compose.yml` — 14 containers: all services + MongoDB + Kafka + ES 8 + Kibana + Redis
- `requirements.txt` — All Python deps (pytesseract, elasticsearch, confluent-kafka, etc.)
- `project_dump.md` — ~81KB full project documentation
- `rules_claude.md` — Implementation rules and constraints
- `discuss.md` — Design discussion notes
- `tests/` — Unit tests: OCR, consumer, stop words
- `ingestion_service_api/images/` — Sample tweet images (tweet_0 through tweet_2)

**Stack:** FastAPI · Kafka (KRaft) · MongoDB 7 · Elasticsearch 8 · Kibana · Redis · GridFS · Streamlit · pytesseract · Docker Compose
