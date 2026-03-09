# Operation Pizza Tray - Microservices Pipeline

A multi-service pizza ordering system built with FastAPI, Kafka, MongoDB, Redis, and Streamlit.
Each pizza order flows through multiple processing stages before reaching its final status.

---

## System Flow

```
                          +------------------+
                          |     CLIENT       |
                          | (uploads JSON)   |
                          +--------+---------+
                                   |
                                   v
                          +------------------+
                          |   API GATEWAY    |  :8000
                          |    (FastAPI)     |
                          +--------+---------+
                                   |
                          +--------+---------+
                          |                  |
                          v                  v
                   +-----------+      +-------------+
                   |  MongoDB  |      |    Kafka     |
                   | (store    |      | topic:       |
                   |  orders)  |      | pizza_orders |
                   +-----------+      +------+-------+
                                             |
                              +--------------+--------------+
                              |                             |
                              v                             v
                   +-------------------+         +-------------------+
                   |  TEXT PROCESSOR   |         |  KITCHEN WORKER   |
                   | (preprocessor)    |         | (cooking sim)     |
                   +--------+----------+         +--------+----------+
                            |                             |
                   1. allergy check                1. wait 15s
                   2. clean text (UPPER,           2. if not BURNT
                      remove punctuation)             -> DELIVERED
                   3. lookup prep from             3. delete Redis
                      pizza_prep.json                 cache key
                            |
                            v
                   +-------------------+
                   |      Kafka        |
                   | topic:            |
                   | cleaned-          |
                   | instructions      |
                   +--------+----------+
                            |
                            v
                   +-------------------+
                   |     ENRICHER      |
                   | (kosher analysis) |
                   +--------+----------+
                            |
                   1. check Redis cache
                      for pizza_type (5s TTL)
                   2. analyze vs closed lists:
                      - forbidden_non_kosher
                      - meat_ingredients
                      - dairy_ingredients
                      - common_allergens
                   3. meat + dairy = not kosher
                   4. if not kosher -> BURNT
                   5. update MongoDB
                            |
                            v
                   +-------------------+
                   |  RISK EVALUATOR   |
                   | (Pandas scanner)  |
                   +--------+----------+
                            |
                   Runs every 10 seconds:
                   1. pull orders into DataFrame
                   2. match special_instructions
                      vs common_allergens
                   3. if allergen match
                      -> CANCELLED (overrides all)
                   4. cache metrics in Redis
                      (dashboard:metrics, 30s TTL)
                            |
                            v
                   +-------------------+
                   |    STREAMLIT      |  :8501
                   |   DASHBOARD      |
                   +-------------------+
                   - Pie chart (status distribution)
                   - Bar chart (top 10 allergens)
                   - Table (last 10 orders)
```

---

## Order Status Lifecycle

```
PREPARING  ->  DELIVERED    (kitchen worker, after 15s)
PREPARING  ->  BURNT        (enricher, if not kosher)
    any    ->  CANCELLED    (risk evaluator, if allergen match - overrides all)
```

---

## Services

| Service            | Port  | Description                                      |
|--------------------|-------|--------------------------------------------------|
| API Gateway        | 8000  | FastAPI - file upload + order lookup              |
| Text Processor     | -     | Kafka consumer - cleans text, flags allergies     |
| Kitchen Worker     | -     | Kafka consumer - simulates cooking, marks DELIVERED |
| Enricher           | -     | Kafka consumer - kosher analysis, marks BURNT     |
| Risk Evaluator     | -     | Polls MongoDB - allergen matching, marks CANCELLED |
| Streamlit Dashboard| 8501  | Visual dashboard with charts and tables           |

---

## Infrastructure

| Service         | Port  | Description              |
|-----------------|-------|--------------------------|
| MongoDB         | 27017 | Primary data store       |
| Mongo Express   | 18081 | MongoDB web UI           |
| MySQL           | 3306  | SQL database             |
| CloudBeaver     | 8978  | SQL web UI               |
| Kafka (KRaft)   | 9092  | Message broker           |
| Kafka UI        | 18080 | Kafka web UI             |
| Redis           | 6379  | Cache (orders + metrics) |
| RedisInsight    | 5540  | Redis web UI             |

---

## Kafka Topics

| Topic                  | Producer        | Consumer(s)               |
|------------------------|-----------------|---------------------------|
| `pizza_orders`         | API Gateway     | Text Processor, Kitchen Worker |
| `cleaned-instructions` | Text Processor  | Enricher                  |

---

## Quick Start

```bash
# start all services
docker compose up --build

# upload orders
curl -X POST http://localhost:8000/api/file_data/uploadfile \
  -F "file=@data/pizza_orders.json"

# check a single order
curl http://localhost:8000/api/file_data/order/ORD001

# open dashboard
# http://localhost:8501
```

---

## Project Structure

```
.
├── api/                        # API Gateway (FastAPI)
│   ├── api.py                  # app entry point
│   ├── router.py               # routes + helpers (upload, lookup, cache)
│   ├── health_routes.py        # health check endpoints
│   └── connection/             # mongo, redis, kafka, mysql clients
│
├── text_processor/             # Text Processor (Kafka consumer)
│   ├── text_worker.py          # main consumer loop (allergy check)
│   ├── clean_preprocessor.py   # cleans text + publishes to kafka
│   └── connection/             # mongo, kafka clients
│
├── kitchen/                    # Kitchen Worker (Kafka consumer)
│   ├── kitchen_worker.py       # cooking simulation + DELIVERED
│   └── connection/             # mongo, redis, kafka clients
│
├── enricher/                   # Enricher (Kafka consumer)
│   ├── enricher_consumer.py    # kosher analysis + BURNT
│   └── connection/             # mongo, redis, kafka clients
│
├── risk_evaluator/             # Risk Evaluator (Pandas scanner)
│   ├── risk_evaluator.py       # allergen matching + CANCELLED
│   └── connection/             # mongo, redis clients
│
├── dashboard/                  # Streamlit Dashboard
│   └── dashboard.py            # pie chart, bar chart, table
│
├── data/                       # Static data files
│   ├── pizza_orders.json       # sample orders (30)
│   ├── pizza_prep.json         # prep instructions per pizza type
│   └── pizza_analysis_lists.json  # closed lists (allergens, kosher, meat, dairy)
│
├── docker-compose.yml          # 14 containers (8 infra + 6 app)
├── Dockerfile                  # shared image (python:3.12-slim)
├── requirements.txt            # python dependencies
├── .env                        # docker-compose variable substitution
├── .env.local                  # local dev environment
└── .env.prod                   # production environment
```
