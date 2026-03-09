# 🍕 Pizza Orders — Elasticsearch Learning Project

A complete ES learning project using real (slightly suspicious) pizza order data.

## Project Structure

```
pizza-es/
├── app/
│   ├── __init__.py
│   ├── config.py          ← env vars (os.getenv with defaults)
│   ├── es_client.py       ← ES connection singleton
│   ├── index_manager.py   ← create index + bulk load data
│   ├── queries.py         ← all ES queries (heavily commented)
│   ├── dal.py             ← data access layer
│   ├── routes.py          ← FastAPI routes
│   └── main.py            ← app entry point + lifespan
├── data/
│   └── pizza_orders.json
├── .env                   ← local environment variables
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── KIBANA_GUIDE.md
└── K8S_GUIDE.md
```

---

## Quick Start

### Option A — Docker Compose (recommended)

```bash
# 1. Start all three services
docker compose up --build

# 2. Wait ~30s for ES to be healthy, then:
#    FastAPI Swagger UI → http://localhost:8000/docs
#    Kibana            → http://localhost:5601

# 3. Stop everything (keep data)
docker compose down

# 4. Stop and wipe all ES data
docker compose down -v
```

### Option B — Local Python (ES must be running separately)

```bash
# Install dependencies
pip install -r requirements.txt

# Set env vars (or edit .env)
export ES_HOST=http://localhost:9200

# Run the app
python -m app.main
# OR
uvicorn app.main:app --reload
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/orders/` | All orders |
| GET | `/orders/{order_id}` | Single order by ID |
| GET | `/orders/search/instructions?q=allergy` | Full-text search |
| GET | `/orders/search/multi?q=chicken` | Multi-field search |
| GET | `/orders/search/fuzzy?q=Peperoni` | Typo-tolerant search |
| GET | `/orders/search/wildcard?pattern=*Chicken*` | Wildcard |
| GET | `/orders/filter/type?pizza_type=Pepperoni` | Exact type match |
| GET | `/orders/filter/delivery?is_delivery=true` | Delivery filter |
| GET | `/orders/filter/quantity?min_qty=2&max_qty=5` | Quantity range |
| GET | `/orders/filter/delivery-by-type?pizza_type=Pepperoni` | Combined filter |
| GET | `/orders/agg/count-by-type` | Orders per type |
| GET | `/orders/agg/quantity-by-type` | Total qty per type |

Full interactive docs: **http://localhost:8000/docs**

---

## Key ES Concepts in This Project

| File | Concept |
|------|---------|
| `index_manager.py` | Mapping, shards, replicas, bulk indexing |
| `queries.py` | match, term, range, bool, multi_match, fuzzy, wildcard, aggregations |
| `es_client.py` | Client singleton, connection pool |
| `dal.py` | Separation of concerns |

---

## Convert to Kubernetes

See **K8S_GUIDE.md** for full instructions.

Quick version:
```bash
# Install kompose
brew install kompose   # macOS

# Convert
kompose convert -f docker-compose.yml -o k8s/

# Apply
kubectl apply -f k8s/
```
