# Pizza Order Pipeline V1 — Kafka + MongoDB + Redis + MySQL

First attempt at the multi-stage pizza order processing pipeline. Orders flow through 5 processing services, each consuming from Kafka and updating order status in MongoDB.

> The refined version of this project is in `../second-attempt/`

---

## System flow

```
Client → API :8000 → MongoDB + Kafka (pizza_orders)
                              ↓              ↓
                     Text Processor     Kitchen Worker
                     (clean + allergy)  (15s cook → DELIVERED)
                              ↓
                     Kafka (cleaned-instructions)
                              ↓
                          Enricher
                     (kosher check → BURNT if meat+dairy)
                              ↓ (polls every 10s)
                     Risk Evaluator
                     (allergen match → CANCELLED, overrides all)
                              ↓
                     Redis (metrics, 30s TTL)
                              ↓
                     Streamlit Dashboard :8501
```

## What's here (`redis_start/`)

- `api/` — FastAPI gateway: upload orders, query status
- `api/connection/` — Kafka, MongoDB, MySQL, Redis clients
- `text_processor/` — Kafka consumer: text cleaning + allergy detection
- `kitchen/` — Kafka consumer: cooking simulation (15s) → DELIVERED
- `enricher/` — Kafka consumer: kosher analysis → BURNT
- `docker-compose.yml` — MongoDB, MySQL, Kafka (KRaft), Redis, CloudBeaver, RedisInsight, Kafka UI, Streamlit
- `STATE.MD` — Implementation state notes
- `requirements.txt` — Python dependencies

## Infrastructure ports

| Service | Port |
|---------|------|
| API Gateway | 8000 |
| Streamlit Dashboard | 8501 |
| Kafka UI | 18080 |
| Mongo Express | 18081 |
| RedisInsight | 5540 |
| CloudBeaver (SQL UI) | 8978 |

**Stack:** FastAPI · Kafka (KRaft) · MongoDB 7 · MySQL 8 · Redis 7 · Pandas · Streamlit · Docker
