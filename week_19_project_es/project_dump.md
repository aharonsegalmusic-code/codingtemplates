# PROJECT TREE

```
.env
analytics/ [subfolders: 0, files: 8, total files: 8]
    __init__.py
    analyticsConfig.py
    analyticsOrchestrator.py
    Dockerfile
    kafkaConsumer.py
    kafkaPublisher.py
    main.py
    textAnalyzer.py
cleaning_consumer/ [subfolders: 0, files: 6, total files: 6]
    __init__.py
    clean_config.py
    clean_orchestrator.py
    Dockerfile
    main.py
    text_cleaner.py
dashboard/ [subfolders: 1, files: 6, total files: 9]
    __init__.py
    APIconfig.py
    connection/ [subfolders: 0, files: 3, total files: 3]
        __init__.py
        mongo_connection.py
        redis_connection.py
    dashboard.py
    Dockerfile
    routes.py
    searchService.py
discuss.md
docker-compose.yml
elastic_consumer/ [subfolders: 0, files: 6, total files: 6]
    __init__.py
    Dockerfile
    indexerConfig.py
    indexOrchestrator.py
    kafkaConsumer.py
    main.py
GridFS_service_api/ [subfolders: 0, files: 7, total files: 7]
    __init__.py
    Dockerfile
    GridFSConfig.py
    GridFsOrchestrator.py
    GridFSStorage.py
    main.py
    routes.py
ingestion_service_api/ [subfolders: 2, files: 9, total files: 22]
    __init__.py
    __pycache__/ [subfolders: 0, files: 10, total files: 10]
        __init__.cpython-314.pyc
        ingestion_config.cpython-314.pyc
        ingestion_orchestrator.cpython-314.pyc
        ingestionConfig.cpython-314.pyc
        kafka_publisher.cpython-314.pyc
        main.cpython-314.pyc
        metadata_extractor.cpython-314.pyc
        mongo_client.cpython-314.pyc
        OCRengine.cpython-314.pyc
        routes.cpython-314.pyc
    Dockerfile
    images/ [subfolders: 0, files: 3, total files: 3]
        tweet_0.png
        tweet_1.png
        tweet_2.png
    ingestion_config.py
    ingestion_orchestrator.py
    main.py
    metadata_extractor.py
    mongo_client.py
    OCRengine.py
    routes.py
README.md
requirements.txt
rules_claude.md
shared/ [subfolders: 1, files: 7, total files: 10]
    __init__.py
    __pycache__/ [subfolders: 0, files: 3, total files: 3]
        __init__.cpython-314.pyc
        kafka_producer.cpython-314.pyc
        logger.cpython-314.pyc
    es_connection.py
    image_model.py
    kafka_consumer.py
    kafka_publisher.py
    logger.py
    mongo_connection.py
tempCodeRunnerFile.py
tests/ [subfolders: 0, files: 3, total files: 3]
    image_test.py
    test_consumer.py
    test_stop_words.py
tweet_0.png
```

# PROJECT STATS

- Total folders: 12
- Total files  : 79

## File types

| Extension | Files | Lines (utf-8 text only) |
|---|---:|---:|
| `.md` | 3 | 765 |
| `.png` | 4 | 0 |
| `.py` | 50 | 1368 |
| `.pyc` | 13 | 0 |
| `.txt` | 1 | 67 |
| `.yml` | 1 | 262 |
| `no_ext` | 7 | 101 |

---

# FILE CONTENTS

## .env

```
MONGO_URI=mongodb://mongo:27017/

ELASTICSEARCH_URL=http://elasticsearch:9200
ELASTICSEARCH_INDEX=images

KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC_RAW=raw
KAFKA_TOPIC_CLEAN=clean
KAFKA_GROUP_CLEAN=cleaning_group
KAFKA_TOPIC_ANALYTIC=analytic
KAFKA_GROUP_INDEXER=Indexer
KAFKA_GROUP_ANALYTIC=analytic_group

GRIDFS_SERVICE_URL=http://GridFS_service:8001

IMAGE_DIRECTORY=/app/images

KAFKA_UI_URL=http://127.0.0.1:18080

MONGO_EXPRESS_URL=http://127.0.0.1:18081

KIBANA_URL=http://127.0.0.1:5601


CLUSTER_ID=Mf_-9PUJQnCI6eQZzgFTlg
MONGO_DB="images_data"
```

## GridFS_service_api/Dockerfile

```
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ ./shared/
COPY GridFS_service_api/ ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

## GridFS_service_api/GridFSConfig.py

```python
"""
loads env 
    -   MongoDb
"""
```

## GridFS_service_api/GridFSStorage.py

```python
"""
stores binary file to MongoDB
"""
```

## GridFS_service_api/GridFsOrchestrator.py

```python
"""
gets POST from Ingestion
saves the binary file in db
"""
```

## GridFS_service_api/__init__.py

```python

```

## GridFS_service_api/main.py

```python
from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="GridFS api",
    version="1.0.0"
)

app.include_router(
    router,
    prefix="/api",
    tags=["GridFS"]
)


@app.get("/")
def root():
    return {"message": "GridFS api is running"}
```

## GridFS_service_api/routes.py

```python
import json
from fastapi import APIRouter
from dotenv import dotenv_values


config = dotenv_values(".env")


router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@router.post("/upload")        # ← same path, same method
def upload(file: UploadFile, image_id: str):
    """
    get from Ingestion a file to be uploaded
    """
```

## README.md

```markdown
# week_19_project_es
elastic search - kafka-data pipline

git commit -m"initial file structure and archtecture including env and compose"
```

## analytics/Dockerfile

```
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ ./shared/
COPY analytics/ ./

CMD ["python", "main.py"]
```

## analytics/__init__.py

```python

```

## analytics/analyticsConfig.py

```python
"""
loads env 
    -   related to kafka
    READ TOPIC: "Clean" 
    WRITE TOPIC: "Analytic" 
"""
```

## analytics/analyticsOrchestrator.py

```python
"""
gets from kafka
anlyzes
produces to kafka
"""
```

## analytics/kafkaConsumer.py

```python
"""
gets Raw image event
"""
```

## analytics/kafkaPublisher.py

```python
"""
publisher clean event 
"""
```

## analytics/main.py

```python

```

## analytics/textAnalyzer.py

```python

```

## cleaning_consumer/Dockerfile

```
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ ./shared/
COPY cleaning_consumer/ ./

CMD ["python", "main.py"]
```

## cleaning_consumer/__init__.py

```python

```

## cleaning_consumer/clean_config.py

```python
"""
loads env 
    -   related to kafka
    READ TOPIC: "raw"
    WRITE TOPIC: "Clean" 
"""
import os


class CleanConfig:

    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
        self.clean_group = os.getenv("KAFKA_GROUP_CLEAN", "cleaning_group")
        self.kafka_topic_raw = os.getenv("KAFKA_TOPIC_RAW", "raw")
        self.kafka_topic_clean = os.getenv("KAFKA_TOPIC_CLEAN", "clean")


```

## cleaning_consumer/clean_orchestrator.py

```python
"""
gets from kafka
passes to be processed 
publishes to kafka
"""

# for local run 
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json

from clean_config import CleanConfig
from shared.logger import get_logger
from shared.kafka_consumer import KafkaConsumerClient
from shared.kafka_publisher import KafkaPublisher 
from text_cleaner import textCleaner

class cleanOrchestrator():
    def __init__(self,
                kafka_consumer,
                kafka_publisher,
                cleaner,
                logger):
        self.kafka_consumer = kafka_consumer
        self.producer = kafka_publisher
        self.cleaner = cleaner
        self.logger = logger

    def get_image(self):
        while True:
            image_data_bin = self.kafka_consumer.poll(5)
            if image_data_bin is None:
                self.logger.info("no message, polling again...")
                continue

            if image_data_bin.error():
                self.logger.error("kafka error: %s", image_data_bin.error())
                continue

            value = image_data_bin.value()
            if not value:
                self.logger.warning("empty message received")
                continue

            image_data = json.loads(value)
            self.logger.info("image id pulled: %s", image_data["image_id"])

            return image_data

    def start_cleaning(self, topic: str):
        self.kafka_consumer.subscribe(topic)
        self.logger.info("cleaning consumer started")

        while True:
            image_data = self.get_image()

            clean_tokens = self.cleaner(image_data["raw_text"])

            event = {
                "image_id": image_data["image_id"],
                "clean_text": clean_tokens,
                "metadata": image_data.get("metadata", {}),
            }

            self.producer.publish(event)
            self.logger.info("published clean event for image_id=%s", image_data["image_id"])


# ---- wiring ----
_logger = get_logger("cleaning-service")
_config = CleanConfig()

orchestrator = cleanOrchestrator(
    kafka_consumer = KafkaConsumerClient(
        bootstrap_servers = _config.bootstrap_servers,
        group_id = _config.clean_group,
        logger = _logger
    ),
    kafka_publisher = KafkaPublisher(_config.bootstrap_servers, _config.kafka_topic_clean, _logger),
    cleaner = textCleaner,
    logger = _logger
)
```

## cleaning_consumer/main.py

```python
"""
RAW event processor
this is the format consumed from kafka

get from -> raw topic

    {'image_id': '32421f607e5c7b53',
    'metadata': {'file_size': 17036,
                'filename': 'tweet_0.png',
                'format': 'PNG',
                'height': 300,
                'mode': 'RGB',
                'width': 600},
    'raw_text': '2020-02-15 17:57:21+00:00\n'
                '\n'
                'AIPAC should be registered as a foreign agent meddling in US\n'
                'elections. American Israel Political Action Committee. It is\n'
                'interfering in the US electoral process and should be put on '
                'trial\n'
                "and it's leaders imprisoned. @benshapiro @charliekirk11\n"
                'https://t.cofebO4iPUah8\n'}
"""
from clean_orchestrator import orchestrator, _config

orchestrator.start_cleaning(_config.kafka_topic_raw)
```

## cleaning_consumer/text_cleaner.py

```python
"""
cleans punctuation and irrelevant chars
"""

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re


nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

def textCleaner(txt):
    # Step 1: Lowercase the entire text
    # "Hello World" -> "hello world"
    txt = txt.lower()

    # Step 2: Remove URLs (anything starting with http or www)
    # "visit https://example.com today" -> "visit  today"
    txt = re.sub(r'http\S+|www\S+', ' ', txt)

    # Step 3: Remove @mentions
    # "@benshapiro said" -> " said"
    txt = re.sub(r'@\S+', ' ', txt)

    # Step 4: Remove anything that is NOT a letter or whitespace
    # removes: . , ! ? ( ) ' " # $ % etc.
    # "it's good." -> "its good"
    txt = re.sub(r'[^a-z\s]', '', txt)

    # Step 5: Collapse multiple spaces into one
    # "hello    world" -> "hello world"
    txt = re.sub(r'\s+', ' ', txt).strip()

    # Get English stopwords and tokenize
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(txt.lower())


    # Remove stopwords
    filtered_tokens = [word for word in tokens if word not in stop_words]

    return filtered_tokens

```

## dashboard/APIconfig.py

```python
"""
loads env 
    - elastic search env
"""
```

## dashboard/Dockerfile

```
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ ./shared/
COPY dashboard/ ./

CMD ["streamlit", "run", "dashboard.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

## dashboard/__init__.py

```python

```

## dashboard/connection/__init__.py

```python

```

## dashboard/connection/mongo_connection.py

```python
import os
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

# --- Config ---
ENV = {**dotenv_values(".env.local"), **os.environ}
MONGO_URI = ENV.get("MONGO_URI", "mongodb://127.0.0.1:27017/")
MONGO_DB = ENV.get("MONGO_DB", "pizza_mongo")


class Mongo:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        self.db: Database = self.client[db_name]

    def collection(self, name: str) -> Collection:
        return self.db[name]

    def close(self):
        self.client.close()


# --- Usage ---
mongo = Mongo(MONGO_URI, MONGO_DB)
```

## dashboard/connection/redis_connection.py

```python
import os
from dotenv import dotenv_values
import redis

ENV = {**dotenv_values(".env.local"), **os.environ}

REDIS_HOST = ENV.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(ENV.get("REDIS_PORT", "6379"))
REDIS_PASSWORD = ENV.get("REDIS_PASSWORD", "") or None

def get_redis_client() -> redis.Redis:
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True,
    )

r = get_redis_client()
```

## dashboard/dashboard.py

```python
"""
Streamlit Dashboard - Pizza Operations Monitor

INPUT:
    - reads all orders from MongoDB (direct query)
    - optionally reads cached metrics from Redis key "dashboard:metrics" (TTL 30s)

OUTPUT:
    - Pie Chart: order status distribution (PREPARING, DELIVERED, BURNT, CANCELLED)
      shows total order count in the title
    - Bar Chart: top 10 allergens that caused CANCELLED orders
    - Table: last 10 orders processed (sorted by update_time desc)
    - Cache indicator: shows whether data came from Redis or MongoDB

FLOW:
    Redis (cache check) -> MongoDB (fallback/fresh data) -> Streamlit UI
    User reloads page to refresh data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pymongo import MongoClient
import os
from dotenv import dotenv_values
import redis

# --- Config ---
ENV = {**dotenv_values(".env.local"), **os.environ}
MONGO_URI = ENV.get("MONGO_URI", "mongodb://127.0.0.1:27017/")
MONGO_DB = ENV.get("MONGO_DB", "pizza_mongo")
REDIS_HOST = ENV.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(ENV.get("REDIS_PORT", "6379"))
REDIS_PASSWORD = ENV.get("REDIS_PASSWORD", "") or None

# --- Connections ---
mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = mongo_client[MONGO_DB]
collection = db["pizza_orders"]

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True,
)


def get_cached_metrics():
    """Try to get pre-computed metrics from Redis cache."""
    try:
        cached = r.get("dashboard:metrics")
        if cached:
            return json.loads(cached), True
    except Exception:
        pass
    return None, False


def compute_metrics_from_mongo():
    """Compute all dashboard metrics directly from MongoDB."""
    orders = list(collection.find({}, {"_id": 0}))
    if not orders:
        return None
    df = pd.DataFrame(orders)
    return df


# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Pizza Operations Dashboard",
    layout="wide"
)

st.title("Pizza Operations Dashboard")

# Check Redis cache first
cached_data, cache_hit = get_cached_metrics()
if cache_hit:
    st.caption("Data source: Redis Cache (fast)")
else:
    st.caption("Data source: MongoDB (fresh query)")

# --- Load data ---
df = compute_metrics_from_mongo()

if df is None or df.empty:
    st.warning("No orders found in MongoDB.")
    st.stop()

# --- Total Orders ---
total_orders = len(df)

# =============================
# ROW 1: Pie Chart + Stats
# =============================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Order Status Distribution")

    if "status" in df.columns:
        status_counts = df["status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]

        fig_pie = px.pie(
            status_counts,
            names="status",
            values="count",
            title=f"Status Distribution (Total Orders: {total_orders})",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No status data available.")

with col2:
    st.subheader("Summary")
    st.metric("Total Orders", total_orders)

    if "status" in df.columns:
        for status, count in df["status"].value_counts().items():
            st.metric(status, count)

# =============================
# ROW 2: Top 10 Allergens Bar Chart
# =============================
st.subheader("Top 10 Allergens (from CANCELLED orders)")

if "allergens_matched" in df.columns and "status" in df.columns:
    cancelled_df = df[df["status"] == "CANCELLED"].copy()

    if not cancelled_df.empty:
        # explode the allergens_matched lists into individual rows
        allergens_series = cancelled_df["allergens_matched"].dropna()

        # handle both list and string types
        all_allergens = []
        for item in allergens_series:
            if isinstance(item, list):
                all_allergens.extend(item)
            elif isinstance(item, str):
                all_allergens.append(item)

        if all_allergens:
            allergen_counts = pd.Series(all_allergens).value_counts().head(10).reset_index()
            allergen_counts.columns = ["allergen", "count"]

            fig_bar = px.bar(
                allergen_counts,
                x="allergen",
                y="count",
                title="Top 10 Allergens Causing Cancellations",
                color="count",
                color_continuous_scale="Reds"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No allergen data found in cancelled orders.")
    else:
        st.info("No CANCELLED orders found.")
else:
    st.info("No allergens_matched data available yet. Run the Risk Evaluator first.")

# =============================
# ROW 3: Last 10 Orders Table
# =============================
st.subheader("Last 10 Orders Processed")

if "update_time" in df.columns:
    recent_df = df.dropna(subset=["update_time"]).sort_values("update_time", ascending=False).head(10)

    # select display columns
    display_cols = ["order_id", "pizza_type", "status", "allergens_matched", "update_time"]
    available_cols = [c for c in display_cols if c in recent_df.columns]

    if not recent_df.empty:
        st.dataframe(
            recent_df[available_cols].reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No orders with update_time found yet.")
else:
    st.info("No update_time data available yet. Run the Risk Evaluator first.")

# --- Footer ---
st.markdown("---")
st.caption(f"Cache status: {'HIT' if cache_hit else 'MISS'} | Auto-refresh: reload page")

# streamlit run dashboard/dashboard.py
```

## dashboard/routes.py

```python
"""
gets requests HTTP
passes them to search service
"""
```

## dashboard/searchService.py

```python
"""
search queries
returns results
"""
```

## discuss.md

```markdown
# Ingestion Service — Code Review & Error Analysis

---

## Overall Assessment

The **logic and structure** of the service is solid. The flow is correct:
`main.py → routes.py → orchestrator → (OCR, metadata, GridFS, Kafka)`.

However, there is **one repeating critical error** that will crash the service at startup — and a few smaller issues.

---

## Critical Error — Repeated in 5 Files

### The Problem: Every module tries to instantiate itself at module-load time, but passes NO arguments to constructors that require them.

Every class in this service has a constructor that **requires** a `logger` (and sometimes more params). Yet at the bottom of each file, an instance is created with **zero arguments**. Python will raise a `TypeError` the moment the module is imported.

| File | Line | Broken Instantiation | What it actually needs |
|---|---|---|---|
| `OCRengine.py` | 46 | `ocr_engine = OCREngine()` | `OCREngine(logger)` |
| `metadata_extractor.py` | 57 | `metadata = MetadataExtractor()` | `MetadataExtractor(logger)` |
| `kafka_publisher.py` | 48 | `publisher = KafkaPublisher()` | `KafkaPublisher(bootstrap_servers, topic_name, logger)` |
| `mongo_client.py` | 51 | `Gridfs = MongoLoaderClient()` | `MongoLoaderClient(gridfs_service_url, logger)` |
| `ingestion_orchestrator.py` | 109 | `orchestrator = IngestionOrchestrator()` | `IngestionOrchestrator(config, ocr_engine, metadata, Gridfs, publisher, logger)` |

**The crash chain:** When Python runs `main.py`, it imports `routes.py`, which imports `ingestion_orchestrator.py`, which imports all the other modules — each one blows up on its last line before any real code even runs.

The error you will see looks like:
```
TypeError: OCREngine.__init__() missing 1 required positional argument: 'logger'
```

---

## Root Cause — Design Mismatch

The **intended design** (documented in every docstring) is **dependency injection**:
- `main.py` creates the logger
- `main.py` builds each component, passing the logger in
- Components are wired together and passed to the orchestrator

**What actually happened:** Every module independently tried to create its own singleton at the bottom, but the logger (and other dependencies) doesn't exist yet at that point.

The fix is simple: `main.py` needs to actually instantiate and wire all the components together — the plumbing that was planned but never written.

---

## Secondary Issues

### 1. `mongo_client.py` — Wrong import path + unused import (line 8)

```python
from ingestion_service_api.ingestion_config import IngestionConfig
```

- All other files use local imports: `from ingestion_config import ...`
- This uses an absolute package path that will fail depending on how the service is run
- **Worse: `IngestionConfig` is imported but never used in this file** — it's dead code

---

### 2. `routes.py` — Confusing self-shadowing variable (lines 7–13)

```python
from ingestion_orchestrator import IngestionOrchestrator
from ingestion_orchestrator import orchestrator

router = APIRouter()
orchestrator: IngestionOrchestrator = orchestrator   # <-- reassigns itself
```

The line `orchestrator: IngestionOrchestrator = orchestrator` is just a type annotation on an import — it does nothing functional. The intent was probably to receive the orchestrator from `main.py` via injection, but that wiring was never built. This is a leftover placeholder.

---

### 3. `main.py` — Logger created but never passed anywhere

```python
logger = get_logger("ingestion-service")
app = FastAPI(title="Ingestion Service")
app.include_router(router)
```

`main.py` creates a logger but never uses it to build any of the service components. The entire wiring step — creating `OCREngine(logger)`, `MetadataExtractor(logger)`, etc. — is missing. The logger just sits there unused.

---

## Summary

| # | Severity | Issue | Location |
|---|---|---|---|
| 1 | CRITICAL | `OCREngine()` called with no args | `OCRengine.py:46` |
| 2 | CRITICAL | `MetadataExtractor()` called with no args | `metadata_extractor.py:57` |
| 3 | CRITICAL | `KafkaPublisher()` called with no args | `kafka_publisher.py:48` |
| 4 | CRITICAL | `MongoLoaderClient()` called with no args | `mongo_client.py:51` |
| 5 | CRITICAL | `IngestionOrchestrator()` called with no args | `ingestion_orchestrator.py:109` |
| 6 | MEDIUM | Wrong import path + unused import | `mongo_client.py:8` |
| 7 | LOW | Logger created but never wired to components | `main.py` |
| 8 | LOW | Redundant self-shadowing orchestrator variable | `routes.py:13` |

---

## What Needs to Happen

`main.py` needs to be the **composition root** — the single place that:
1. Creates the logger
2. Creates the config
3. Creates each component (OCREngine, MetadataExtractor, MongoLoaderClient, KafkaPublisher) — passing the logger and config values in
4. Creates the orchestrator — passing all components in
5. Passes the orchestrator to the router

The classes themselves are written correctly. The wiring between them is what's missing.
```

## docker-compose.yml

```yaml
#############################################################################################################
##################################+---------------------------+##############################################
##################################|     ~  IMAGES   ~         |##############################################
##################################+---------------------------+##############################################
#############################################################################################################

services:
# +--------------------+
# |       MONGO        |
# +--------------------+
  mongo:
    image: mongo:7
    restart: unless-stopped
    ports:
      - "27017:27017" # TODO change if port 27017 is already used
    volumes:
      - mongo_data:/data/db
    command: mongod --noauth
    environment:
      MONGO_INITDB_DATABASE: ${MONGO_DB}
    networks:
      - app-network

# +--------------------+
# |   MONGO UI (WEB)   |
# +--------------------+
  mongo-express:
    image: mongo-express:1.0.2
    restart: unless-stopped
    ports:
      - "18081:8081" # TODO change if port 8081 is already used
    environment:
      ME_CONFIG_MONGODB_SERVER: mongo
      ME_CONFIG_MONGODB_ENABLE_LOGIN: "false"
      ME_CONFIG_BASICAUTH: "false"
    depends_on:
      - mongo
    networks:
      - app-network

# +--------------------+
# |       KAFKA        |
# +--------------------+
  kafka:
    image: confluentinc/cp-kafka:7.6.1
    restart: unless-stopped
    ports:
      - "9092:9092" # TODO change if port 9092 is already used
    environment:
      CLUSTER_ID: ${CLUSTER_ID}
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: "broker,controller"
      KAFKA_CONTROLLER_QUORUM_VOTERS: "1@kafka:9093"

      # listeners
      KAFKA_LISTENERS: "PLAINTEXT://0.0.0.0:29092,PLAINTEXT_HOST://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093"
      KAFKA_ADVERTISED_LISTENERS: "PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092" # TODO if you change host port 9092, update this
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: "PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT,CONTROLLER:PLAINTEXT"
      KAFKA_INTER_BROKER_LISTENER_NAME: "PLAINTEXT"
      KAFKA_CONTROLLER_LISTENER_NAMES: "CONTROLLER"

      # single node dev defaults
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
    networks:
      - app-network

# +--------------------+
# |      KAFKA UI      |
# +--------------------+
  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    restart: unless-stopped
    ports:
      - "18080:8080" # TODO change if port 8080 is already used
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: "kafka:29092"
    depends_on:
      - kafka
    networks:
      - app-network


# +--------------------+
# |   Elasticsearch    |
# +--------------------+
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
    ports:
      - "9200:9200"
    volumes:
      - esdata:/usr/share/elasticsearch/data
    networks:
      - app-network

# +--------------------+
# |   Kibana           |
# +--------------------+
  kibana:
    image: docker.elastic.co/kibana/kibana:8.12.0
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
    networks:
      - app-network

# +--------------------+
# | STREAMLIT DASHBOARD|
# +--------------------+
  streamlit_dashboard:
    build:
      context: .
      dockerfile: dashboard/Dockerfile
    restart: unless-stopped
    ports:
      - "8501:8501"
    environment:
      MONGO_URI: mongodb://mongo:27017/
      MONGO_DB: ${MONGO_DB}
      ELASTICSEARCH_URL: "http://elasticsearch:9200"    
      ELASTICSEARCH_INDEX: "images"
    depends_on:
      - mongo
      - elasticsearch                                    
    networks:
      - app-network

#############################################################################################################
##################################+---------------------------+##############################################
##################################|     ~   CODE   ~          |##############################################
##################################+---------------------------+##############################################
#############################################################################################################

# +------------------------+
# | cleaning_consumer py   |
# +------------------------+
  cleaning_consumer:
    build:
      context: .
      dockerfile: cleaning_consumer/Dockerfile
    # so it only loads once
    # restart: "no"
    depends_on:
      - kafka
    environment:
      KAFKA_BOOTSTRAP_SERVERS: "kafka:29092"
      KAFKA_TOPIC_RAW: "raw"
      KAFKA_TOPIC_CLEAN: "clean"
      KAFKA_GROUP_CLEAN: "cleaning_group"
    networks:
      - app-network

# +--------------------------+
# | elastic_consumer PY      |
# +--------------------------+
  elastic_consumer:
    build:
      context: .
      dockerfile: elastic_consumer/Dockerfile
    restart: unless-stopped
    depends_on:
      - kafka
      - elasticsearch
    environment:
      KAFKA_BOOTSTRAP_SERVERS: "kafka:29092"
      KAFKA_TOPIC_RAW: "raw"
      KAFKA_TOPIC_CLEAN: "clean"
      KAFKA_TOPIC_ANALYTIC: "analytic"
      KAFKA_GROUP_INDEXER: "Indexer"
      ELASTICSEARCH_URL: "http://elasticsearch:9200"   
      ELASTICSEARCH_INDEX: "images"                    

    networks:
      - app-network
# +--------------------+
# |  analytics PY      |
# +--------------------+
  analytics:
    build:
      context: .
      dockerfile: analytics/Dockerfile
    restart: unless-stopped
    depends_on:
      - kafka
    environment:
      KAFKA_BOOTSTRAP_SERVERS: "kafka:29092"
      KAFKA_TOPIC_CLEAN: "clean"
      KAFKA_TOPIC_ANALYTIC: "analytic"
      KAFKA_GROUP_ANALYTIC: "analytic_group"

    networks:
      - app-network
    
# +--------------------+
# |  ingestion_service |
# +--------------------+

  ingestion_service:
    build:
      context: .
      dockerfile: ingestion_service_api/Dockerfile
    restart: unless-stopped
    ports:
      - "8000:8000"
    depends_on:
      - kafka
      - gridfs_service
    environment:
      KAFKA_BOOTSTRAP_SERVERS: "kafka:29092"
      KAFKA_TOPIC_RAW: "raw"
      GRIDFS_SERVICE_URL: "http://gridfs_service:8001"
      IMAGE_DIRECTORY: "/app/images"                                

    networks:
      - app-network

# +--------------------+
# |  GridFS_service    |
# +--------------------+
  gridfs_service:
    build:
      context: .
      dockerfile: GridFS_service_api/Dockerfile
    restart: unless-stopped
    ports:
      - "8001:8001"
    depends_on:
      - mongo
    environment:
      MONGO_URI: "mongodb://mongo:27017/"               
      MONGO_DB: ${MONGO_DB}  
    networks:
      - app-network

#############################################################################################################
##################################+---------------------------+##############################################
##################################|     ~  DEPS     ~         |##############################################
##################################+---------------------------+##############################################
#############################################################################################################


volumes:
  mongo_data:
  esdata:

networks:
  app-network:
    driver: bridge
```

## elastic_consumer/Dockerfile

```
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ ./shared/
COPY elastic_consumer/ ./

CMD ["python", "main.py"]
```

## elastic_consumer/__init__.py

```python

```

## elastic_consumer/indexOrchestrator.py

```python
"""
manages flow 
applies upsert by image_id
"""
# for local run 
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json

from shared.logger import get_logger
from shared.kafka_consumer import KafkaConsumerClient
from shared.kafka_publisher import KafkaPublisher 
from shared.es_connection import get_es_client

from indexerConfig import elasticConfig

class indexOrchestrator():
    def __init__(self,
                es_connection,
                kafka_consumer,
                consumer_topics,
                logger):
        self.es_connection = es_connection
        self.kafka_consumer = kafka_consumer
        self.consumer_topics = consumer_topics
        self.logger = logger

    def get_image(self):
        while True:
            image_data_bin = self.kafka_consumer.poll(5)
            if image_data_bin is None:
                self.logger.info("no message, polling again...")
                continue

            if image_data_bin.error():
                self.logger.error("kafka error: %s", image_data_bin.error())
                continue

            value = image_data_bin.value()
            if not value:
                self.logger.warning("empty message received")
                continue

            image_data = json.loads(value)
            self.logger.info("image id pulled: %s", image_data["image_id"])

            return image_data
    
    def poll_and_index(self, index: str):
        self.kafka_consumer.subscribe(self.consumer_topics)
        self.logger.info("index consumer started — listening to %s", self.consumer_topics)

        while True:
            image_data = self.get_image()
            image_id = image_data["image_id"]

            self.es_connection.update(
                index=index,
                id=image_id,
                body={"doc": image_data, "doc_as_upsert": True}
            )
            self.logger.info("upserted image_id=%s", image_id)

            

# ---- wiring ----
_logger = get_logger("index-service")
_config = elasticConfig()

orchestrator = indexOrchestrator(
    es_connection = get_es_client(),
    kafka_consumer = KafkaConsumerClient(
        bootstrap_servers = _config.bootstrap_servers,
        group_id = _config.indexer_group,
        logger = _logger
    ),
    consumer_topics = _config.kafka_topics_raw_clean,
    logger = _logger
)
```

## elastic_consumer/indexerConfig.py

```python
"""
loads env 
    -   related to kafka
    READ TOPIC: "RAW"
    READ TOPIC: "Clean"
    READ TOPIC: "Analytic"
    KAFKA_GROUP_INDEXER: "Indexer"

    - elastic search env



get from -> raw topic

    {'image_id': '32421f607e5c7b53',
    'metadata': {'file_size': 17036,
                'filename': 'tweet_0.png',
                'format': 'PNG',
                'height': 300,
                'mode': 'RGB',
                'width': 600},
    'raw_text': '2020-02-15 17:57:21+00:00\n'
                '\n'
                'AIPAC should be registered as a foreign agent meddling in US\n'
                'elections. American Israel Political Action Committee. It is\n'
                'interfering in the US electoral process and should be put on '
                'trial\n'
                "and it's leaders imprisoned. @benshapiro @charliekirk11\n"
                'https://t.cofebO4iPUah8\n'}
"""
import os


class elasticConfig:

    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
        self.indexer_group = os.getenv("KAFKA_GROUP_INDEXER", "Indexer")
        self.kafka_topics_raw_clean = [os.getenv("KAFKA_TOPIC_RAW", "raw"),os.getenv("KAFKA_TOPIC_CLEAN", "clean")]
        self.es_index = os.getenv("ELASTICSEARCH_INDEX", "images")

        self.mapping =   {
                        "mappings": {
                            "properties": {
                                'image_id':     {"type": "keyword"},  
                                'filename':     {"type": "keyword"},     
                                'format':       {"type": "keyword"}, 
                                'height':       {"type": "integer"}, 
                                'mode':         {"type": "keyword"},   
                                'width':        {"type": "integer"}, 
                                'raw_text':     {"type": "text"}, 
                                'clean_text':   {"type": "text"}, 
                            }
                        }
                    }


```

## elastic_consumer/kafkaConsumer.py

```python
"""
gets Raw image event
"""
```

## elastic_consumer/main.py

```python
"""
gets from 3 topics
            raw
            clean
            analytics
stores them as one image id with 3 versions of it
"""

from indexOrchestrator import orchestrator, _config

orchestrator.poll_and_index(_config.es_index)
```

## ingestion_service_api/Dockerfile

```
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ ./shared/
COPY ingestion_service_api/ ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## ingestion_service_api/OCRengine.py

```python
"""
OCRengine.py
Extracts text from an image using pytesseract
Constructor: logger
"""

from logging import Logger
from pathlib import Path


from PIL import Image
import pytesseract


class OCREngine:

    def __init__(self, logger: Logger):
        self.logger = logger

    def extract_text(self, image_path: str) -> str:
        """
        Run OCR on the given image file.

        Args:
            image_path: Path to the image file.

        Returns:
            raw_text extracted from the image.
        """
        self.logger.info("Running OCR on: %s", Path(image_path).name)

        try:
            img = Image.open(image_path)
            raw_text = pytesseract.image_to_string(img)
            self.logger.info(
                "OCR complete for %s — extracted %d characters",
                Path(image_path).name,
                len(raw_text),
            )
            return raw_text

        except Exception as e:
            self.logger.error("OCR failed for %s: %s", image_path, e)
            raise

```

## ingestion_service_api/__init__.py

```python

```

## ingestion_service_api/__pycache__/OCRengine.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service_api/__pycache__/__init__.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service_api/__pycache__/ingestionConfig.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service_api/__pycache__/ingestion_config.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service_api/__pycache__/ingestion_orchestrator.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service_api/__pycache__/kafka_publisher.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service_api/__pycache__/main.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service_api/__pycache__/metadata_extractor.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service_api/__pycache__/mongo_client.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service_api/__pycache__/routes.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service_api/images/tweet_0.png

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service_api/images/tweet_1.png

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service_api/images/tweet_2.png

**SKIPPED (binary or non-UTF8 text)**

## ingestion_service_api/ingestion_config.py

```python
"""
ingestionConfig.py
Loads environment variables for the Ingestion Service.
Constructor: no params — loads from env.
"""

import os


class IngestionConfig:

    def __init__(self):
        self.image_directory = os.getenv("IMAGE_DIRECTORY", "images")
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.kafka_topic_raw = os.getenv("KAFKA_TOPIC_RAW", "raw")
        self.gridfs_service_url = os.getenv("GRIDFS_SERVICE_URL", "http://localhost:8001")

config = IngestionConfig()
```

## ingestion_service_api/ingestion_orchestrator.py

```python
"""
ingestion_orchestrator.py
Scans the local image directory, processes each image end-to-end.
Constructor: config, ocr_engine, metadata_extractor, Gridfs, publisher, logger
"""

import os
import sys
from logging import Logger
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.logger import get_logger
from ingestion_config import IngestionConfig
from OCRengine import OCREngine
from metadata_extractor import MetadataExtractor
from mongo_client import MongoLoaderClient
from shared.kafka_publisher import KafkaPublisher

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif", ".webp"}


class IngestionOrchestrator:

    def __init__(
        self,
        config: IngestionConfig,
        ocr_engine: OCREngine,
        metadata: MetadataExtractor,
        Gridfs: MongoLoaderClient,
        publisher: KafkaPublisher,
        logger: Logger,
    ):
        self.config = config
        self.ocr_engine = ocr_engine
        self.metadata_extractor = metadata
        self.Gridfs = Gridfs
        self.publisher = publisher
        self.logger = logger

    def process_image(self, path: str) -> None:
        """
        Process a single image end-to-end:
        1. Generate image_id
        2. Extract metadata
        3. Run OCR
        4. Send binary to GridFS service
        5. Publish RAW event to Kafka
        """
        filename = Path(path).name
        self.logger.info("Processing image: %s", filename)

        try:
            # 1. generate unique image_id
            image_id = self.metadata_extractor.generate_image_id(path)

            # 2. extract metadata
            metadata = self.metadata_extractor.extract_metadata(path)

            # 3. run OCR
            raw_text = self.ocr_engine.extract_text(path)
    
            # 4. publish RAW event
            event = {
                "image_id": image_id,
                "raw_text": raw_text,
                "metadata": metadata,
            }
            self.publisher.publish(event)

            # 5. send binary file to GridFS service
            self.Gridfs.send(path, image_id)


            self.logger.info("Finished processing image_id=%s (%s)", image_id, filename)

        except Exception as e:
            self.logger.error("Failed to process %s: %s", filename, e)

    def run(self) -> dict:
        """
        Scan the image directory and process all image files.

        Returns:
            Summary dict with processed/failed counts.
        """
        image_dir =self.config.image_directory
        self.logger.info("Scanning image directory: %s", image_dir)

        files = [
            os.path.join(image_dir, f)
            for f in os.listdir(image_dir)
            if Path(f).suffix.lower() in IMAGE_EXTENSIONS
        ]

        self.logger.info("Found %d image files", len(files))

        processed = 0
        failed = 0

        for file_path in files:
            try:
                self.process_image(file_path)
                processed += 1
            except Exception:
                failed += 1

        summary = {"processed": processed, "failed": failed, "total": len(files)}
        self.logger.info("Ingestion complete: %s", summary)
        return summary


# ---- wiring ----
_logger = get_logger("ingestion-service")
_config = IngestionConfig()

orchestrator = IngestionOrchestrator(
    config=_config,
    ocr_engine=OCREngine(_logger),
    metadata=MetadataExtractor(_logger),
    Gridfs=MongoLoaderClient(_config.gridfs_service_url, _logger),
    publisher=KafkaPublisher(_config.bootstrap_servers, _config.kafka_topic_raw, _logger),
    logger=_logger,
)
```

## ingestion_service_api/main.py

```python
"""
main.py
Ingestion Service entry point.
"""
from fastapi import FastAPI
from routes import router

app = FastAPI(title="Ingestion Service")
app.include_router(router)


```

## ingestion_service_api/metadata_extractor.py

```python
"""
metadata_extractor.py
Extracts basic metadata from an image file and generates a unique image_id.
Constructor: logger
"""

import os
from logging import Logger
from pathlib import Path
import hashlib


from PIL import Image



class MetadataExtractor:

    def __init__(self, logger: Logger):
        self.logger = logger

    def extract_metadata(self, image_path: str) -> dict:
        """
        Extract basic metadata from the image file.

        Returns:
            dict with keys: filename, file_size, width, height, format
        """
        with Image.open(image_path) as img:
            metadata = {
                "filename": os.path.basename(image_path),
                "format": img.format,
                "width": img.size[0],
                "height": img.size[1],
                "mode": img.mode,             
                "file_size": os.path.getsize(image_path),
            }
            return metadata

    def generate_image_id(self, image_path: str) -> str:
        """
        Generate a unique ID from file content.
        Same file = same ID.
        """
        # open file in binary mode and read all bytes
        with open(image_path, "rb") as f:
            file_bytes = f.read()

        # hashlib.sha256(file_bytes)  → creates a hash object from the bytes
        # .hexdigest()                → converts hash to a 64-character string like "a3f2b1c8..."
        # [:16]                       → take first 16 characters — short but still unique
        image_id = hashlib.sha256(file_bytes).hexdigest()[:16]
        return image_id
```

## ingestion_service_api/mongo_client.py

```python
"""
Sends the binary file to the GridFS Service via HTTP POST.
Constructor: gridfs_service_url, logger
"""

from logging import Logger
from pathlib import Path
import requests

class MongoLoaderClient:

    def __init__(self, gridfs_service_url: str, logger: Logger):
        self.gridfs_service_url = gridfs_service_url.rstrip("/")
        self.logger = logger

    def send(self, file_path: str, image_id: str) -> dict:
        """
        POST the binary file to the GridFS service.

        Args:
            file_path: Path to the image file.
            image_id:  Unique identifier for the image.

        Returns:
            Response JSON from the GridFS service.
        """
        filename = Path(file_path).name
        url = f"{self.gridfs_service_url}/upload"

        self.logger.info("Sending %s (image_id=%s) to %s", filename, image_id, url)

        # open file in binary mode and send as multipart form data
        # files = the binary image
        # data  = the image_id so GridFS knows what to name it
        with open(file_path, "rb") as f:
            response = requests.post(
                url,
                files={"file": (filename, f)},
                data={"image_id": image_id},
                timeout=30,
            )

        # raise an exception if status code is 4xx or 5xx
        response.raise_for_status()

        self.logger.info("Upload success for image_id=%s", image_id)
        return response.json()

```

## ingestion_service_api/routes.py

```python
"""
routes.py
FastAPI routes for the Ingestion Service.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from ingestion_orchestrator import orchestrator

router = APIRouter()


@router.post("/ingest")
def ingest_all():
    """Scan the image directory and process all images."""
    summarry = orchestrator.run()
    return summarry

# @router.post("/ingest/single")
# def ingest_single(file: UploadFile = File(...)):
#     """
#     Upload and process a single image.
#     Saves to IMAGE_DIRECTORY then processes it.
#     """
#     pass


@router.get("/health")
def health():
    return {"status": "healthy", "service": "ingestion-service"}
```

## requirements.txt

```
altair==6.0.0
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.12.1
attrs==25.4.0
blinker==1.9.0
cachetools==6.2.6
certifi==2026.1.4
charset-normalizer==3.4.4
click==8.3.1
colorama==0.4.6
confluent==0.3.2
confluent-kafka==2.13.0
dnspython==2.8.0
elastic-transport==8.17.1
elasticsearch==8.19.3
fastapi==0.129.2
gitdb==4.0.12
GitPython==3.1.46
h11==0.16.0
idna==3.11
Jinja2==3.1.6
joblib==1.5.3
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
kafka==1.3.5
MarkupSafe==3.0.3
multipart==1.3.0
narwhals==2.16.0
nltk==3.9.2
numpy==2.4.2
packaging==26.0
pandas==2.3.3
pillow==12.1.1
protobuf==6.33.5
pyarrow==23.0.1
pydantic==2.12.5
pydantic_core==2.41.5
pydeck==0.9.1
pymongo==4.16.0
pytesseract==0.3.13
python-dateutil==2.9.0.post0
python-dotenv==1.2.1
pytz==2025.2
PyYAML==6.0.3
redis==7.2.0
referencing==0.37.0
regex==2026.2.19
requests==2.32.5
rpds-py==0.30.0
schema==0.7.8
six==1.17.0
smmap==5.0.2
sniffio==1.3.1
starlette==0.52.1
streamlit==1.54.0
tenacity==9.1.4
toml==0.10.2
tornado==6.5.4
tqdm==4.67.3
typing-inspection==0.4.2
typing_extensions==4.15.0
tzdata==2025.3
urllib3==2.6.3
uvicorn==0.41.0
watchdog==6.0.0
```

## rules_claude.md

```markdown
# project generation rules for educational backend templates

this file defines the rules you must follow when generating an educational project.
it is a rules document only and does not request any code by itself.
remember this is for educational purposes so keep in a learning level stardard priortuze simplisity and clarity over indusrty hight standards 
---

## 1 format rules
- start with making the folder and file structure
i dont want it overcomplcated, make the filestructe clear and simple 

add a test folder 
for each feature make a test 
meaning a verry simple individual run demonstring a logic section 
lets say we need to procces a images in teh program so in the test we will have one imge going throgh the flow in simple steps one function to do the process 
think of it as if i were making a feature and testing it in a micro way is seperate 
so for each logic/feature in the code make a file and a simle test for it 
in each test file a a cler docstring of the flow and whats happening 
if a library is used then a verry short explnation of the library 

add a run md file on all i need to know about how to run the code 
---

## 2 language and tooling rules
- all application code must be written in python
- comments and documentation must be in english
- bash commands are allowed only in clearly marked markdown code blocks labeled `bash`
- do not include any hebrew text in the response

---

## 3 python code style rules
- keep the code very simple and beginner friendly
- prefer clarity over performance and advanced tricks
- do not use advanced patterns
  - no complex abstractions
  - no design patterns beyond simple classes for connection wrappers
- async usage rule
  - default: do not use async functions
    - only regular synchronous functions using `def`
  - exception: if i explicitly request beanie
    - you may use `async def` and `await` only in the service(s) that require beanie
    - keep all other services fully synchronous
    - do not introduce async just for style or symmetry
    - if there is a striclty needed reason to use asynt then make 2 file one caleed file with async and then the file that is taking the risk but this file with no async will be the defualt 
- do not use type hints anywhere
  - no `: str`, `: list`, and no `-> something`
  - exception: pydantic models require type hints for field definitions, that is ok
- use capital letters only where python or libraries require or convention suggests
  - example `FastAPI` import is ok
  - for custom class names you may keep them lowercase for simplicity
- comments in code must follow these strict rules
  - only lowercase letters are allowed in comments
  - comment lines must not end with punctuation dots

---

## 4 architecture rules

### 4.1 service structure
- if there are multiple services then the project must be structured as multiple services in separate folders
- each service must be usable and testable as an independent unit
- each service should be small and focused with these files
  - `main.py` or a descriptive name like `worker.py` for the entry point
  - `router.py` for api endpoints (only if the service is a web api)
  - `connection/` folder for all database and broker connections (see section 8)
  - `__init__.py` in each package folder (empty, no logic)

### 4.2 project root
- `docker-compose.yml` at root
- `.env` at root for docker-compose variable substitution
- `data/` folder at root for any shared static json or seed data
- `README.md` at root with the system flow

---

## 5 data access and sql rules

### general guidelines
- do not use orm features or magic methods
- always use plain sql strings for database operations
- keep sql very simple and readable
- sql keywords must be written in CAPITAL LETTERS
  - examples: SELECT, FROM, WHERE, INSERT INTO, VALUES, ORDER BY, GROUP BY

### sql style constraints
- only return the columns explicitly requested in the task
- do not add extra context columns unless explicitly asked
- no aliases
  - avoid AS
  - avoid short table names like c or co
  - always use full table and column names like country.Name
- no subqueries, ctes, derived tables, or window functions unless explicitly allowed
- use a single SELECT statement with optional JOIN, WHERE, GROUP BY, HAVING, and ORDER BY

### commenting rules for sql
- always include a short clear comment explaining what the query does in order of execution
- example style
  - `# join cities to countries, left join official country languages, select city country language, order by country and city`
- comments should be simple readable and directly match the sql query logic
- do not describe internal ids or joins unless they appear in the output

---

## 6 sql documentation file rule
- if the project includes any sql in code
  - you must also include a dedicated markdown file for sql commands only
  - it must recreate the exact sql queries used in code
  - each query must be labeled like this
    - `note -- problem number and basic description`
  - then provide the complete working query inside a sql code block

---

## 7 error handling rules
- do not add any error handling unless explicitly requested
- assume all inputs and services work correctly
- exception: health check endpoints may use try/except to report service status

---

## 8 connection modules rules

every service that connects to an external system (database, broker, cache) must have a
`connection/` subfolder with a dedicated module per connection type.
each connection module follows these rules:

### 8.1 environment variables in connection modules
use `os.environ.get("VAR_NAME", "local_default_value")` to read config.
the local default value is what you use during local development.
in docker/production, the env var is set in docker-compose and overrides the default.

```python
import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://127.0.0.1:27017/")
MONGO_DB = os.environ.get("MONGO_DB", "my_database")
```

do not use `dotenv_values`, do not use `.env.local` files, do not merge dicts.
just `os.environ.get("KEY", "default")` and nothing else.

### 8.2 mongodb connection module
file: `<service>/connection/mongo_connection.py`

```python
import os
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://127.0.0.1:27017/")
MONGO_DB = os.environ.get("MONGO_DB", "my_database")


class Mongo:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        self.db = self.client[db_name]

    def collection(self, name):
        return self.db[name]

    def close(self):
        self.client.close()


mongo = Mongo(MONGO_URI, MONGO_DB)
```

usage in service code:
```python
from .connection.mongo_connection import mongo

collection = mongo.collection("orders")
```

### 8.3 redis connection module
file: `<service>/connection/redis_connection.py`

```python
import os
import redis

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "") or None


def get_redis_client():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True,
    )


r = get_redis_client()
```

usage in service code:
```python
from .connection.redis_connection import r

r.set("key", "value", ex=60)
cached = r.get("key")
```

### 8.4 kafka producer connection module
file: `<service>/connection/kafka_connection_producer.py`

```python
import os
from confluent_kafka import Producer

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")


class KafkaProducerClient:
    def __init__(self, bootstrap_servers):
        self.producer = Producer({"bootstrap.servers": bootstrap_servers})

    def send(self, topic, value):
        self.producer.produce(topic=topic, value=value)

    def flush(self):
        self.producer.flush()


producer = KafkaProducerClient(KAFKA_BOOTSTRAP_SERVERS)
```

usage in service code:
```python
from .connection.kafka_connection_producer import producer
import json

value = json.dumps(data).encode("utf-8")
producer.send("my_topic", value)
producer.flush()
```

### 8.5 kafka consumer connection module
file: `<service>/connection/kafka_connection_consumer.py`

each consumer service gets its own group id so kafka tracks offsets independently.

```python
import os
from confluent_kafka import Consumer

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")
KAFKA_GROUP_ID = os.environ.get("KAFKA_GROUP_ID_MYSERVICE", "my-service-group")


class KafkaConsumerClient:
    def __init__(self, bootstrap_servers, group_id):
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })

    def subscribe(self, topic):
        self.consumer.subscribe([topic])

    def poll(self, timeout=1.0):
        return self.consumer.poll(timeout)

    def close(self):
        self.consumer.close()


consumer = KafkaConsumerClient(KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID)
```

### 8.6 mysql connection module
file: `<service>/connection/mysql_connection.py`

```python
import os
import mysql.connector

MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", "3306"))
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD", "root_pwd")
MYSQL_DB = os.environ.get("MYSQL_DATABASE", "my_database")


def get_mysql_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        connection_timeout=3
    )
```

### 8.7 module instantiation rule
- every connection module must create a global instance at the bottom of the file
- other code imports that instance directly
- this keeps things simple: one import, ready to use

---

## 9 kafka patterns

### 9.1 consumer loop pattern
every kafka consumer service must follow this exact loop structure:

```python
import json

TOPIC = os.environ.get("TOPIC_NAME", "my-topic")

collection = mongo.collection("my_collection")
consumer.subscribe(TOPIC)


def process():
    print("service_name running...")
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"consumer error: {msg.error()}")
                continue

            data = json.loads(msg.value())

            # process the message here

    finally:
        consumer.close()


process()
```

rules:
- poll timeout is always `1.0` seconds
- always check `if msg is None: continue`
- always check `if msg.error()` and print the error
- always parse with `json.loads(msg.value())`
- always wrap in `try/finally` with `consumer.close()` in finally
- always call the function at module level at the bottom of the file

### 9.2 producer send pattern
every kafka publish must follow this pattern:

```python
import json

value = json.dumps(data_dict).encode("utf-8")
producer.send(TOPIC, value)
producer.flush()
```

rules:
- always convert dict to json string then encode to utf-8 bytes
- always call `flush()` after each `send()`

---

## 10 mongodb patterns

### 10.1 insert
```python
collection.insert_one(document_dict)
```

### 10.2 find one
```python
# exclude _id from results
result = collection.find_one({"order_id": some_id}, {"_id": 0})
```

### 10.3 find many
```python
cursor = collection.find(
    {"status": {"$ne": "DONE"}},
    {"_id": 0, "order_id": 1, "status": 1}
)
results = list(cursor)
```

### 10.4 update one
```python
collection.update_one(
    {"order_id": some_id},
    {"$set": {"status": "COMPLETED", "updated_at": timestamp}}
)
```

rules:
- always use `{"_id": 0}` in projections to exclude mongo internal id
- always use `$set` for updates
- filter is always the first argument, update/projection is second

---

## 11 redis cache-aside pattern

whenever a service needs to cache data, use this exact pattern:

```python
import json

# check cache
cached = r.get(cache_key)
if cached:
    result = json.loads(cached)
    # use cached result
else:
    result = fetch_from_database()
    r.set(cache_key, json.dumps(result), ex=TTL_SECONDS)
    # use fresh result
```

for cache invalidation (when data changes):
```python
r.delete(cache_key)
```

rules:
- always serialize to json before storing in redis: `json.dumps()`
- always deserialize after reading: `json.loads()`
- always set a ttl with `ex=seconds`
- always use `r.delete(key)` when data becomes stale

---

## 12 fastapi patterns

### 12.1 app entry point
file: `<service>/main.py`

```python
from fastapi import FastAPI
from .router import router

app = FastAPI(
    title="my service",
    version="1.0.0"
)

app.include_router(
    router,
    prefix="/api",
    tags=["main"]
)


@app.get("/")
def root():
    return {"message": "service is running"}
```

### 12.2 router module
file: `<service>/router.py`

```python
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
import json
from .connection.mongo_connection import mongo
from .connection.redis_connection import r

router = APIRouter(
    prefix="/data",
    tags=["data"],
)


# pydantic model for validation
class Item(BaseModel):
    item_id: str
    name: str
    status: str = "PENDING"


@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    data = json.loads(file.file.read())
    # process data
    return {"count": len(data)}


@router.get("/item/{item_id}")
def get_item(item_id):
    # use cache-aside pattern here
    return item
```

### 12.3 health check router (optional)
file: `<service>/health_routes.py`

```python
from fastapi import APIRouter
from .connection.mongo_connection import mongo
from .connection.redis_connection import get_redis_client

health_router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@health_router.get("/mongo")
def ping_mongo():
    try:
        collections = mongo.db.list_collection_names()
        return {"status": "ok", "service": "mongo"}
    except Exception as e:
        return {"status": "error", "service": "mongo", "message": str(e)}
```

rules:
- pydantic models are defined inside the router file, not in a separate models file
- file upload uses `UploadFile = File(...)`
- routers are mounted with `app.include_router(router, prefix=..., tags=[...])`
- pydantic type hints are the only allowed type hints in the project
- use `model.model_dump()` to convert pydantic model to dict

---

## 13 docker rules

### 13.1 per-service dockerfile
every service must have its own dockerfile inside its folder.
each dockerfile copies only the code that service needs.

file: `<service>/Dockerfile`

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY <service>/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY <service>/ ./<service>/
CMD ["python", "-m", "<service>.main"]
```

if the service needs shared data files:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY <service>/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY <service>/ ./<service>/
COPY data/ ./data/
CMD ["python", "-m", "<service>.main"]
```

for fastapi services:
```dockerfile
CMD ["uvicorn", "<service>.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

for streamlit services:
```dockerfile
CMD ["streamlit", "run", "<service>/dashboard.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

### 13.2 per-service requirements.txt
every service must have its own `requirements.txt` with only the dependencies it actually uses.
do not install packages the service does not import.

### 13.3 docker-compose service definition
use `context` and `dockerfile` to point to each service's own dockerfile:

```yaml
my_service:
    build:
      context: .
      dockerfile: my_service/Dockerfile
    restart: unless-stopped
    environment:
      MONGO_URI: mongodb://mongo:27017/
      MONGO_DB: ${MONGO_DB}
      REDIS_HOST: redis
      REDIS_PORT: 6379
    depends_on:
      - mongo
      - redis
    networks:
      - app-network
```

rules:
- `context: .` is always the project root so COPY paths work
- `dockerfile:` points to the service-specific dockerfile
- no `command:` override needed since CMD is in the dockerfile
- environment variables here override `os.environ.get()` defaults in code
- all services must be on the same docker network
- infrastructure services (mongo, redis, kafka) come first in the file
- application services come after infrastructure

### 13.4 .env file for docker-compose
the `.env` file at root is only for docker-compose `${VAR}` substitution.
it contains the values that docker-compose.yml references with `${...}` syntax.

```
MONGO_DB=my_database
REDIS_PORT=6379
KAFKA_BOOTSTRAP_SERVERS=kafka:29092
```

---

## 14 docstring rules

every main entry point file of a service must have a docstring at the top with this format:

```python
"""
Service Name - Short Description

INPUT:
    - what this service receives (kafka topic, api endpoint, database poll)

OUTPUT:
    - what this service produces (database updates, kafka messages, api responses)

FLOW:
    source -> this service -> destination
"""
```

---

## 15 readme rules

every project must have a `README.md` at the root with:
- project title and one-line description
- ascii flow diagram showing the full data pipeline
- table of services with ports and descriptions
- table of infrastructure with ports
- table of message broker topics with producer and consumer columns
- quick start section with docker compose command and example curl/api calls
- project structure tree showing all folders and key files
```

## shared/__init__.py

```python

```

## shared/__pycache__/__init__.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## shared/__pycache__/kafka_producer.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## shared/__pycache__/logger.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## shared/es_connection.py

```python
"""
es_connection.py
Shared Elasticsearch connection factory.

Usage:
    from es_connection import get_es_client

    es = get_es_client(logger=logger)
    es.index(index="images", id="123", document={...})
"""

import os
from logging import Logger
from elasticsearch import Elasticsearch


def get_es_client(
    url: str | None = None,
    logger: Logger | None = None,
) -> Elasticsearch:
    """
    Create and verify an Elasticsearch client.

    Args:
        url:    Elasticsearch URL. Falls back to ELASTICSEARCH_URL env var.
        logger: Optional logger for connection status.

    Returns:
        Connected Elasticsearch client.

    Raises:
        ConnectionError: If Elasticsearch is unreachable.
    """
    url = url or os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

    es = Elasticsearch(url)

    # verify connection
    if not es.ping():
        msg = f"Elasticsearch is unreachable at {url}"
        if logger:
            logger.error(msg)
        raise ConnectionError(msg)

    if logger:
        info = es.info()
        logger.info(
            "Connected to Elasticsearch %s at %s (cluster: %s)",
            info["version"]["number"],
            url,
            info["cluster_name"],
        )

    return es
```

## shared/image_model.py

```python
class ImageData:
    def _init_(self, image_id, imageName, file_size_bytes, width, height, file_format, path, text):
        self.image_id = image_id
        self.imageName = imageName
        self.file_size_bytes = file_size_bytes
        self.width = width
        self.height = height
        self.file_format = file_format
        self.path = path
        self.text = text
```

## shared/kafka_consumer.py

```python
from confluent_kafka import Consumer
from logging import Logger

class KafkaConsumerClient:
    def __init__(self, bootstrap_servers: str, group_id: str,logger: Logger):
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })
        self.logger = logger

    def subscribe(self, topics):
        if isinstance(topics, str):
            topics = [topics]
        self.consumer.subscribe(topics)
        self.logger.info("subscribed to %s", topics)


    def poll(self, timeout: float = 1.0):
        self.logger.info("did poll")
        return self.consumer.poll(timeout)

    def close(self):
        self.logger.info("close consumer")
        self.consumer.close()

# consumer = KafkaConsumerClient(KAFKA_BOOTSTRAP_SERVERS,KAFKA_GROUP_ID_TEXT)

```

## shared/kafka_publisher.py

```python
"""
shared/kafka_publisher.py
Generic Kafka publisher — reused by all services.
Constructor: bootstrap_servers, topic_name, logger
"""

from logging import Logger
import json

from confluent_kafka import Producer


class KafkaPublisher:

    def __init__(self, bootstrap_servers: str, topic_name: str, logger: Logger):
        self.producer = Producer({"bootstrap.servers": bootstrap_servers})
        self.topic_name = topic_name
        self.logger = logger
        self.logger.info("KafkaPublisher ready — topic: %s", topic_name)

    def publish(self, event: dict) -> None:
        image_id = event.get("image_id", "unknown")
        self.logger.info("Publishing event for image_id=%s to %s", image_id, self.topic_name)

        try:
            self.producer.produce(
                topic=self.topic_name,
                key=image_id,
                value=json.dumps(event).encode("utf-8"),
            )
            self.producer.flush()
            self.logger.info("Published image_id=%s", image_id)

        except Exception as e:
            self.logger.error("Failed to publish event: %s", e)
            raise
```

## shared/logger.py

```python
"""
shared/logger.py

Creates a logger for a service.
Each service creates ONE logger in main.py and passes it to all components.
This replaces print() everywhere.

Usage:
    from shared.logger import get_logger
    logger = get_logger("ingestion-service")
    logger.info("started")
    logger.error("something broke")
"""

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """
    Args:
        name: the service name — shows up in every log line.
              example: "ingestion-service", "cleaning-consumer"
    """

    logger = logging.getLogger(name)
    #  minimum level -> "show everything"
    logger.setLevel(logging.DEBUG)

    # don't add handlers twice if called again with the same name
    if logger.handlers:
        return logger

    # format:  2026-02-23 14:05:01 | INFO     | ingestion-service:process_image:45 - message
    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # print to terminal
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(fmt)
    logger.addHandler(handler)

    return logger
```

## shared/mongo_connection.py

```python
from dotenv import dotenv_values
from pymongo import MongoClient

class Mongo:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        self.db = self.client[db_name]

    def collection(self, name):
        return self.db[name]

    def close(self):
        self.client.close()


# mongo = Mongo(MONGO_URI, MONGO_DB)
```

## tempCodeRunnerFile.py

```python
ret = {}
with Image.open("tweet_0.png") as file:
    info = file.getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
print(ret)
```

## tests/image_test.py

```python
from PIL import Image, ExifTags
import pytesseract
from PIL.ExifTags import TAGS
import os
import hashlib
from pprint import pprint


dir_path = "ingestion_service_api\images"
image_path = "tweet_0.png"

def extract_metadata(image_path: str) -> dict:
    """
    Extract basic metadata from the image file.

    Returns:
        dict with keys: filename, file_size, width, height, format
    """
    with Image.open(image_path) as img:
        metadata = {
            "filename": os.path.basename(image_path),
            "format": img.format,
            "width": img.size[0],
            "height": img.size[1],
            "mode": img.mode,             
            "file_size": os.path.getsize(image_path),
        }
        return metadata

def generate_image_id(image_path: str) -> str:
    """
    Generate a unique ID from file content.
    Same file = same ID.
    """
    # open file in binary mode and read all bytes
    with open(image_path, "rb") as f:
        file_bytes = f.read()

    # hashlib.sha256(file_bytes)  → creates a hash object from the bytes
    # .hexdigest()                → converts hash to a 64-character string like "a3f2b1c8..."
    # [:16]                       → take first 16 characters — short but still unique
    image_id = hashlib.sha256(file_bytes).hexdigest()[:16]
    return image_id


def extract_text(image_path: str) -> str:
    """
    Run OCR on the given image file.

    Args:
        image_path: Path to the image file.

    Returns:
        raw_text extracted from the image.
    """
    try:
        img = Image.open(image_path)
        raw_text = pytesseract.image_to_string(img)
        return raw_text

    except Exception as e:
        raise

metadata = extract_metadata(image_path)
image_id = generate_image_id(image_path)
raw_text = extract_text(image_path)
event = {
    "image_id": image_id,
    "raw_text": raw_text,
    "metadata": metadata,
}
print("-----------EVENT--------------")
pprint(event)
```

## tests/test_consumer.py

```python
from confluent_kafka import Consumer
from logging import Logger
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import time
from shared.logger import get_logger

class KafkaConsumerClient:
    def __init__(self, bootstrap_servers: str, group_id: str,logger: Logger):
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })
        self.logger = logger

    def subscribe(self, topic: str):
        self.consumer.subscribe([topic])
        self.logger.info("subscribed to %s", topic)


    def poll(self, timeout: float = 1.0):
        self.logger.info("did poll")
        return self.consumer.poll(timeout)

    def close(self):
        self.logger.info("close consumer")
        self.consumer.close()

class CleanConfig:

    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.clean_group = os.getenv("KAFKA_GROUP_CLEAN", "cleaning_group")
        self.kafka_topic_raw = os.getenv("KAFKA_TOPIC_RAW", "RAW")
        self.kafka_topic_clean = os.getenv("KAFKA_TOPIC_CLEAN", "clean")

logger = get_logger("testing")
config = CleanConfig()
consumer = KafkaConsumerClient(config.bootstrap_servers,config.clean_group,logger)
consumer.subscribe(config.kafka_topic_raw)

found = 0
while True:
    image_data_bin = consumer.poll(5)
    if image_data_bin is None:
        print("consume attempt complete")
        continue

    if image_data_bin.error():
        logger.error("kafka error: %s", image_data_bin.error())
        continue

    value = image_data_bin.value()
    if not value:
        logger.warning("empty message received")
        continue

    image_data = json.loads(value)
    print(image_data)
    print("consume complete")
```

## tests/test_stop_words.py

```python
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re


nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')


txt = """AIPAC should be registered as a foreign agent meddling in US
elections. American Israel Political Action Committee. It is
interfering in the US electoral process and should be put on trial
and it's leaders imprisoned. @benshapiro @charliekirk11
https://t.cofebO4iPUah8"""

# Step 1: Lowercase the entire text
# "Hello World" -> "hello world"
txt = txt.lower()

# Step 2: Remove URLs (anything starting with http or www)
# "visit https://example.com today" -> "visit  today"
txt = re.sub(r'http\S+|www\S+', ' ', txt)

# Step 3: Remove @mentions
# "@benshapiro said" -> " said"
txt = re.sub(r'@\S+', ' ', txt)

# Step 4: Remove anything that is NOT a letter or whitespace
# removes: . , ! ? ( ) ' " # $ % etc.
# "it's good." -> "its good"
txt = re.sub(r'[^a-z\s]', '', txt)

# Step 5: Collapse multiple spaces into one
# "hello    world" -> "hello world"
txt = re.sub(r'\s+', ' ', txt).strip()

# Get English stopwords and tokenize
stop_words = set(stopwords.words('english'))
tokens = word_tokenize(txt.lower())


# Remove stopwords
filtered_tokens = [word for word in tokens if word not in stop_words]

print("Filtered:", filtered_tokens)
```

## tweet_0.png

**SKIPPED (binary or non-UTF8 text)**

