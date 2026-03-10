# AUTONOMOUS CODE GENERATION TASK

**Source:** project_1
**Received:** 2026-03-10T14:33:44.965806+00:00
**Mode:** NEW PROJECT
**Working directory:** C:\Users\a0527\claude-pipeline-work\codingtemplates\20260310_221825

---

## CRITICAL OPERATING RULES — READ FIRST

You are running in FULLY AUTONOMOUS headless mode. These rules are absolute:

1. **NEVER ask questions.** NEVER request clarification. NEVER pause for user input.
2. **If instructions are unclear or ambiguous, MAKE YOUR OWN DECISION.** Do not stop.
3. **Create `dilemmas.md`** at the project root. For EVERY uncertain decision, document:
   - What the dilemma was
   - What options you considered
   - Which option you chose
   - Why you chose it
   If there are no dilemmas, create the file with "No dilemmas encountered."
4. **Do NOT create `complete.md`** — that file is created separately by the pipeline. If you create it, it will be overwritten.
5. **All code must be complete and functional.** No TODOs, no placeholders, no "implement this later".
6. **Include a `README.md`** with clear setup and run instructions.
7. **Include dependency files** (requirements.txt, package.json, etc.) as appropriate.
8. **Work entirely inside the current working directory** (C:\Users\a0527\claude-pipeline-work\codingtemplates\20260310_221825). Do not write files outside of it.

---

## OUTPUT LOCATION

Generate ALL code inside this directory:
```
C:\Users\a0527\claude-pipeline-work\codingtemplates\20260310_221825\9.template_max\projects\project_1
```
Create it if it doesn't exist. Do NOT generate files in the repo root or anywhere else.

---

## INTERMEDIATE GIT COMMITS

You MUST commit AND push your progress as you work — do NOT wait until the end.

After each major section run these shell commands:
```bash
git add -A
git commit -m "progress: [brief description of what you just completed]"
git push
```

Commit and push at minimum after:
- Creating the initial folder and file structure
- Completing each major feature or service
- Writing tests or documentation

The user watches your commits appearing in real-time via `git pull`.

---

## PERMANENT CODING RULES


# project generation rules for educational backend templates

this file defines the rules you must follow when generating an educational project.
it is a rules document only and does not request any code by itself.
remember this is for educational purposes so keep everything at a learning-level standard.
prioritize simplicity and clarity over industry high standards.

---

## 1 output rules
- claude code builds the entire project directly — folders, files, and all code
- start by creating the folder and file structure first
- then fill in the code file by file

---

## 2 language and tooling rules
- all application code must be written in python
- comments and documentation must be in english
- bash commands are allowed only in clearly marked markdown code blocks labeled `bash`
- do not include any hebrew text in any generated file
- always prefer the simplest, most beginner-friendly library for any task
  - use the kind of tools found on geeksforgeeks or w3schools tutorials
  - do not use complex industry-grade or cloud-based tools unless explicitly requested
  - examples of correct choices:
    - ocr: `pytesseract` not google cloud vision
    - audio to text: `speech_recognition` with `recognize_google` not whisper or deepgram
    - http requests: `requests` not httpx or aiohttp
    - image processing: `Pillow` not opencv unless needed
  - the code should look like something a student would write following a tutorial

---

## 3 python code style rules
- keep the code very simple and beginner friendly
- prefer clarity over performance and advanced tricks
- do not use advanced patterns
  - no complex abstractions
  - no design patterns beyond simple classes for connection wrappers and orchestrators
- the code must not look ai-generated
  - no overly verbose or decorative comments
  - no "helper" naming patterns like `_helper`, `_util`, `_handler` unless truly needed
  - no unnecessary wrapper functions or abstractions
  - no comments that just repeat what the code obviously does (like `# create logger` above `logger = get_logger()`)
  - keep it natural — like a student wrote it, not a machine
- async usage rule
  - default: do not use async functions — only regular synchronous functions using `def`
  - exception: if i explicitly request beanie you may use `async def` and `await` only in the service(s) that require beanie
  - keep all other services fully synchronous
  - do not introduce async just for style or symmetry
  - if there is a strictly needed reason to use async then make 2 files — one with async and one without — the file without async is the default
- do not use type hints anywhere
  - no `: str`, `: list`, and no `-> something`
  - exception: pydantic models require type hints for field definitions — that is ok
- use capital letters only where python or libraries require or convention suggests
  - example `FastAPI` import is ok
  - for custom class names you may keep them lowercase for simplicity
- comments in code must follow these strict rules
  - only lowercase letters are allowed in comments
  - comment lines must not end with punctuation dots
- variable and parameter naming must be clear and descriptive
  - no unclear shortened names like `fs`, `es`, `f`, `r`, `db`
  - use full descriptive names that explain what the variable is
  - examples of bad names: `fs`, `es`, `f`, `r`, `msg`
  - examples of good names: `gridfs_storage`, `elasticsearch_client`, `file_handle`, `redis_client`, `kafka_message`
  - exception: loop variables like `i`, `j` in simple for loops are ok
  - exception: well-known standard abbreviations in their original context are ok (e.g. `os`, `sys`, `json`)

---

## 4 architecture rules

### 4.1 project root
- `docker-compose.yml` at root
- `.env` at root for docker-compose variable substitution
- `data/` folder at root for any shared static json or seed data
- `shared/` folder at root (see section 4.3)
- `tests/` folder at root (see section 4.4)
- `connection_tests/` folder at root (see section 4.5)
- `doc/` folder at root (see section 4.6)
- `requirements.txt` at root — single file with all dependencies for the whole project
- `0.general/` folder at root — personal templates and assets, completely unrelated to the project
  - must be in `.gitignore` and `.dockerignore`
  - never reference, read, copy, or use anything from this folder
  - never include it in any dockerfile, docker-compose, or code
  - pretend it does not exist

### 4.2 service structure
- if there are multiple services then the project must be structured as multiple services in separate folders
- each service must be usable and testable as an independent unit
- each service should be small and focused with these files
  - `main.py` for the entry point (minimal — just imports and calls)
  - `<name>_orchestrator.py` for the main logic flow — receives all dependencies via constructor
  - `<name>_config.py` for environment variable loading — simple class using `os.getenv()`
  - `router.py` for api endpoints (only if the service is a web api)
  - `Dockerfile` inside the service folder
  - `__init__.py` in each package folder (empty, no logic)
- wiring section — lives at the bottom of the orchestrator file, not in main.py
  - creates the logger via `shared/logger.py`
  - creates the config
  - creates each component passing dependencies in
  - assembles the orchestrator with all components
- `main.py` just imports the assembled orchestrator and calls it

### naming convention for services
- services that **only save or move data** without transforming it should be named by their data flow
  - examples: `file_to_mongo_es`, `data_to_redis`, `events_to_postgres`
  - these services just read from one place and write to another — no modification of the data itself
- services that **transform, modify, extract from, or enrich data** should use action words like processor, transcriber, analyzer, etc
  - examples: `audio_transcriber`, `text_processor`, `image_analyzer`
  - these services change the data, add to it, or extract new information from it
- do not use vague names like `file_processor` for a service that only saves data

### 4.3 shared folder
the `shared/` folder at root contains reusable modules used by multiple services:
- `logger.py` — creates a logger with `get_logger("service-name")`, replaces print() everywhere
- `kafka_consumer.py` — shared kafka consumer class
- `kafka_publisher.py` — shared kafka publisher class
- `mongo_connection.py` — shared mongo connection class
- `es_connection.py` — shared elasticsearch connection (only if project uses elasticsearch)
- any shared data models
- `__init__.py` (empty)

every service imports from shared — for example:
```python
from shared.logger import get_logger
from shared.kafka_publisher import KafkaPublisher
```

every dockerfile must copy the shared folder into the container:
```dockerfile
COPY shared/ ./shared/
```

if a service also needs connection modules specific to itself (for example a dashboard needing its own mongo/redis connections), it can have a `connection/` subfolder inside the service folder.

### 4.4 tests folder
- `tests/` folder at root
- for each logic/feature in the code make a file with a simple test for it
- tests are simple standalone scripts — not pytest style — just run directly with `python tests/test_name.py`
- each test demonstrates one feature/flow in a micro way in isolation
- example: if the program processes images, the test has one image going through the flow in simple steps — one function per process step
- each test file must have a clear docstring explaining the flow and what is happening
- if a library is used in the test then add a very short explanation of the library
- demo files rule: if the test needs input files (images, audio, json, etc.) — use real demo files provided by the user. never create dummy or fake files. if no demo files were provided, ask the user for them
- every test file must clearly separate simulation code from actual project code using big visible comments like this:

```python
# ============================================================
# SIMULATION SETUP — this code is not part of the main project
# it only exists to set up the test environment
# ============================================================
temp_file = tempfile.NamedTemporaryFile(suffix=".wav")
# ... setup code ...

# ============================================================
# ACTUAL PROJECT CODE — this is the real logic from the project
# from: file_ingestor/ingestor_orchestrator.py
# ============================================================
path = Path(temp_file.name)
metadata = {
    "file_name": path.name,
    "file_size": path.stat().st_size,
}
# ... actual logic ...

# ============================================================
# SIMULATION VERIFICATION — checking the results
# ============================================================
print("metadata:", metadata)
```

this makes it immediately clear what is the real code being demonstrated and what is just scaffolding

### 4.5 connection_tests folder
- `connection_tests/` folder at root
- purpose: verify that all infrastructure services (kafka, mongo, elasticsearch, redis, mysql, etc.) are reachable and configured correctly
- this folder is not part of the project runtime — it is a standalone diagnostic tool
- one file per infrastructure dependency:
  - `test_kafka.py` — connects to kafka, creates a test topic, produces and consumes a test message, then cleans up
  - `test_mongo.py` — connects to mongo, inserts a test document, reads it back, then deletes it
  - `test_elasticsearch.py` — connects to elasticsearch, indexes a test document, searches for it, then deletes it
  - (add more as needed per project: `test_redis.py`, `test_mysql.py`, etc.)
- one combined file: `test_all.py` — runs all connection checks in sequence, prints a summary of what passed and what failed
- each file must:
  - print clear success/failure messages
  - if a connection fails, print the error and a suggested fix (like "make sure mongo is running on port 27017")
  - clean up anything it creates (delete test documents, topics, etc.)
- these tests run locally against running infrastructure — run with `python connection_tests/test_mongo.py`
- the connection config in these files uses the same `os.getenv()` pattern with local defaults from the rules

### 4.6 doc folder
- `doc/` folder at root
- contains all markdown documentation files for the project:
  - `README.md` — project overview, flow diagram, service table, infra table, topics table, quick start, project structure
  - `run.md` — how to run the project
    - must include a "local setup" section explaining how to create a venv, activate it, and install requirements.txt
    - infrastructure (kafka, mongo, etc.) runs via docker-compose, but python code and tests run locally against it
    - terminal on windows is git bash — all commands should work in git bash
    - include activation command for git bash: `source venv/Scripts/activate`
  - `project_state.md` — tracks the current state of the project (files, services, infrastructure, task log)
  - any sql documentation files (if the project uses sql)
  - any other markdown documentation
- `doc/` must be in `.gitignore` and `.dockerignore`
- this folder is for documentation only — no code, no config, no runtime files
- `project_state.md` must be updated by claude code at the end of every task (see section 4.7)

### 4.7 project_state.md update rule
- at the end of every task, claude code must update `doc/project_state.md`
- update the following sections:
  - `current status` — last updated date, total tasks completed, total files
  - `task log` — add a new row for the completed task
  - `file list` — add any new files created in this task
  - `tech stack` — add any new tools introduced
  - `infrastructure` — add any new infrastructure services
  - `application services` — add any new app services
  - `kafka topics` — add any new topics
  - `project structure` — update the tree to reflect current state
  - `detailed summary` — update the description if the system changed

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
- aliases are allowed — use `AS` for readable column and table names
- subqueries are allowed where they make the query clearer
- CTEs (common table expressions) are encouraged — use the `WITH` syntax to define named subqueries at the top, then use them in the main query below. this is the preferred style for complex queries
- window functions are not allowed unless explicitly requested
- a query can use JOIN, WHERE, GROUP BY, HAVING, ORDER BY, subqueries, and CTEs freely

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

## 7 error handling and extra code rules
- do not add any error handling unless explicitly requested
- assume all inputs and services work correctly
- exception: health check endpoints may use try/except to report service status
- the goal is bare minimum code — only what is strictly needed to fulfill the task
- if you add any code that is not part of the bare minimum mandatory logic — such as:
  - input filtering or validation (like glob patterns, type checks)
  - defensive defaults or safety checks
  - fallback values or retry logic
  - any extra robustness not explicitly asked for
- then you must:
  1. mark it with a visible comment block like this:
  ```python
  # --------------------------------------------------------
  # EXTRA: input filtering — not explicitly requested
  # reason: prevents processing non-wav files that might be in the folder
  # source: implied by task saying "list all .wav files"
  # --------------------------------------------------------
  wav_files = list(folder.glob("*.wav"))
  ```
  2. state the source — one of:
     - `explicitly requested` — the task instructions said to do this
     - `implied by task` — the task said something general that could mean this
     - `added by claude` — not in the instructions at all, added for safety/robustness
  3. explain briefly why it is there
- this applies to all code in the project — services, shared modules, tests, everything
- when in doubt, keep the code minimal and do not add extras

---

## 8 connection modules rules

### 8.1 shared connections vs service-specific connections
- reusable connection clients (kafka consumer, kafka publisher, mongo, elasticsearch) go in the `shared/` folder
- these shared clients receive their config via constructor parameters — they do not read env vars themselves
- each service's config class reads the env vars and passes them to the shared clients during wiring
- if a service needs a connection only it uses (like dashboard needing redis), it can have a `connection/` subfolder

### 8.2 environment variables
use `os.getenv("VAR_NAME", "local_default_value")` or `os.environ.get("VAR_NAME", "local_default_value")` to read config.
the local default value is what you use during local development.
in docker/production, the env var is set in docker-compose and overrides the default.

```python
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/")
MONGO_DB = os.getenv("MONGO_DB", "my_database")
```

do not use `dotenv_values`, do not use `.env.local` files, do not merge dicts.
just `os.getenv("KEY", "default")` and nothing else.

**config class attribute naming:** attributes on a config class must use UPPERCASE names that match the env var they load. config values are constants — they are set once at startup and never change, so UPPERCASE is the correct python convention.

```python
class IngestorConfig:
    def __init__(self):
        self.KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
        self.KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "file-events")
        self.ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
        self.LOG_INDEX = os.getenv("LOG_INDEX", "system-logs")
```

### 8.3 shared logger module
file: `shared/logger.py`

the logger writes to both stdout and elasticsearch. every log entry is also indexed in elasticsearch for monitoring via kibana. the ES handler is built into the logger class so any `logger.info()` or `logger.error()` call automatically goes to both stdout and ES — no extra code needed in the services.

```python
import logging
from elasticsearch import Elasticsearch
from datetime import datetime


class Logger:

    _logger = None

    @classmethod
    def get_logger(cls, name="podcast-system", es_host="http://localhost:9200",
                   log_index="system-logs", level=logging.DEBUG):
        if cls._logger:
            return cls._logger

        logger = logging.getLogger(name)
        logger.setLevel(level)

        if not logger.handlers:
            elasticsearch_client = Elasticsearch(es_host)

            class ESHandler(logging.Handler):
                def emit(self, record):
                    try:
                        elasticsearch_client.index(index=log_index, document={
                            "timestamp": datetime.utcnow().isoformat(),
                            "level": record.levelname,
                            "logger": record.name,
                            "message": record.getMessage()
                        })
                    except Exception as error:
                        print(f"es log failed: {error}")

            logger.addHandler(ESHandler())
            logger.addHandler(logging.StreamHandler())

        cls._logger = logger
        return logger
```

usage in any service:
```python
from shared.logger import Logger

logger = Logger.get_logger(
    name="file-to-mongo-es",
    es_host=config.es_host,
    log_index=config.log_index
)
logger.info("service started")
logger.error("failed to store file: %s", error_message)
```

rules:
- every success must be logged with `logger.info()`
- every failure must be logged with `logger.error()` including the error type and full message
- the `es_host` and `log_index` come from each service's config class
- the logger is a singleton — `get_logger()` returns the same instance after the first call
- all services import `Logger` from `shared.logger` and call `Logger.get_logger()`

### 8.4 shared kafka publisher
file: `shared/kafka_publisher.py`

```python
import json
from confluent_kafka import Producer


class KafkaPublisher:

    def __init__(self, bootstrap_servers, topic_name, logger):
        self.producer = Producer({"bootstrap.servers": bootstrap_servers})
        self.topic_name = topic_name
        self.logger = logger

    def publish(self, event):
        value = json.dumps(event).encode("utf-8")
        self.producer.produce(topic=self.topic_name, value=value)
        self.producer.flush()
        self.logger.info("published to %s", self.topic_name)
```

### 8.5 shared kafka consumer
file: `shared/kafka_consumer.py`

```python
import json
from confluent_kafka import Consumer


class KafkaConsumerClient:

    def __init__(self, bootstrap_servers, group_id, logger):
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

    def get_message(self):
        while True:
            kafka_message = self.consumer.poll(5)
            if kafka_message is None:
                self.logger.info("no message, polling again...")
                continue
            if kafka_message.error():
                self.logger.error("kafka error: %s", kafka_message.error())
                continue
            value = kafka_message.value()
            if not value:
                self.logger.warning("empty message received")
                continue
            return json.loads(value)

    def close(self):
        self.consumer.close()
```

`get_message()` blocks until a valid message arrives and returns a plain python dict. the poll loop, error checking, and json decoding all live here — orchestrators do not repeat this logic.

### 8.6 shared mongo connection
file: `shared/mongo_connection.py`

```python
from pymongo import MongoClient


class Mongo:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        self.db = self.client[db_name]

    def collection(self, name):
        return self.db[name]

    def close(self):
        self.client.close()
```

### 8.7 shared elasticsearch connection
file: `shared/es_connection.py`

```python
from elasticsearch import Elasticsearch


class ElasticsearchClient:

    def __init__(self, host):
        self.client = Elasticsearch(host)

    def setup_index(self, index_name, mapping):
        if not self.client.indices.exists(index=index_name):
            self.client.indices.create(index=index_name, body=mapping)

    def index_document(self, index_name, doc_id, document):
        self.client.index(index=index_name, id=doc_id, document=document)

    def close(self):
        self.client.close()
```

`setup_index()` must be called once at service startup (in the wiring section) before any documents are indexed. it creates the index with explicit field type mappings only if it does not already exist. explicit mappings prevent elasticsearch from guessing field types via dynamic mapping, which causes issues with `keyword` vs `text` fields in filters and aggregations.

example mapping for the podcast-metadata index:
```python
mapping = {
    "mappings": {
        "properties": {
            "file_name":        {"type": "keyword"},
            "file_size":        {"type": "integer"},
            "created_at":       {"type": "keyword"},
            "modified_at":      {"type": "keyword"},
            "file_path":        {"type": "keyword"},
            "transcription":    {"type": "text"},
            "bds_percent":      {"type": "float"},
            "is_bds":           {"type": "boolean"},
            "bds_threat_level": {"type": "keyword"}
        }
    }
}
elasticsearch_client.setup_index(config.ES_INDEX, mapping)
```

### 8.8 shared redis connection
file: `shared/redis_connection.py`

```python
import redis


class RedisClient:

    def __init__(self, host, port, password=None):
        self.client = redis.Redis(
            host=host,
            port=port,
            password=password,
            decode_responses=True
        )

    def push(self, queue_name, value):
        self.client.lpush(queue_name, value)

    def peek(self, queue_name):
        return self.client.lindex(queue_name, 0)

    def pop(self, queue_name):
        return self.client.rpop(queue_name)

    def get_all(self, queue_name):
        return self.client.lrange(queue_name, 0, -1)

    def remove(self, queue_name, value):
        self.client.lrem(queue_name, 1, value)

    def set_value(self, key, value, ttl=None):
        self.client.set(key, value, ex=ttl)

    def get_value(self, key):
        return self.client.get(key)

    def delete_key(self, key):
        self.client.delete(key)

    def increment(self, key):
        return self.client.incr(key)

    def close(self):
        self.client.close()
```

queue behavior: `push()` uses LPUSH, `pop()` uses RPOP — together this gives FIFO (first in, first out) queue behavior. for stack (LIFO) behavior, use `push()` + LPOP instead.

the class also includes basic key-value methods (set_value, get_value, delete_key, increment) for caching and counters.

### 8.9 shared mysql connection
file: `shared/mysql_connection.py`

```python
import mysql.connector


class MySQLClient:

    def __init__(self, host, port, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            connection_timeout=3
        )
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
```

---

## 9 kafka patterns

### 9.1 consumer loop pattern in orchestrator
`get_message()` now lives in `KafkaConsumerClient` (see section 8.5). orchestrators do not repeat the poll loop. every kafka consumer service must follow this structure:

```python
def start(self, topic):
    self.kafka_consumer.subscribe(topic)
    self.logger.info("consumer started, waiting for messages...")
    while True:
        data = self.kafka_consumer.get_message()
        self.logger.info("pulled: %s", data.get("file_name", "unknown"))
        self.process(data)
```

### 9.2 producer send pattern
every kafka publish must follow this pattern via the shared publisher:

```python
event = {"key": "value"}
self.publisher.publish(event)
```

the shared publisher handles json encoding, producing, and flushing internally.

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

### 10.5 gridfs — store and retrieve binary files
use gridfs when storing large binary files like audio, images, or pdfs in mongodb.

store a file:
```python
import gridfs

fs = gridfs.GridFS(mongo.db)
with open(file_path, "rb") as f:
    file_id = fs.put(f, filename=file_name, doc_id=unique_id)
```

retrieve a file:
```python
out = fs.find_one({"doc_id": unique_id})
data = out.read()
```

rules:
- always pass a custom identifier (like `doc_id`) as extra metadata when storing
- this lets you find the file later without relying on the gridfs internal `_id`
- use `fs.find_one()` with your custom field to retrieve
- always open files in binary mode (`"rb"`) when storing

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
from routes import router

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
    return {"count": len(data)}


@router.get("/item/{item_id}")
def get_item(item_id):
    return item
```

### 12.3 health check endpoint
```python
@router.get("/health")
def health():
    return {"status": "healthy", "service": "my-service"}
```

rules:
- pydantic models are defined inside the router file, not in a separate models file
- file upload uses `UploadFile = File(...)`
- routers are mounted with `app.include_router(router, prefix=..., tags=[...])`
- pydantic type hints are the only allowed type hints in the project
- use `model.model_dump()` to convert pydantic model to dict

### 12.4 sql fastapi pattern (database + dal + router)

when a fastapi service queries a sql database, use this three-layer pattern:

#### database class
file: `<service>/database.py`

the database class handles all connection management — open, close, cursor, commit, rollback. no sql queries live here.

```python
import os
import mysql.connector
from mysql.connector import Error

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root_pwd")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "podcast_db")


class Database:

    def __init__(self):
        self.host = DB_HOST
        self.port = DB_PORT
        self.user = MYSQL_USER
        self.password = MYSQL_PASSWORD
        self.database = MYSQL_DATABASE

    def _get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )

    def query(self, sql, params=None):
        if params is None:
            params = ()
        conn = None
        cursor = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return rows
        except Error as error:
            print("database query error:", error)
            raise
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass

    def execute(self, sql, params=None):
        if params is None:
            params = ()
        conn = None
        cursor = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
        except Error as error:
            print("database execute error:", error)
            if conn is not None:
                conn.rollback()
            raise
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass


db = Database()
```

#### table config
file: `<service>/table_config.py`

all CREATE TABLE statements live here. run at service startup to ensure tables exist. tables must have auto-increment primary keys and foreign key relationships where applicable.

```python
from database import db


def setup_tables():
    # main table with auto increment id
    db.execute("""
        CREATE TABLE IF NOT EXISTS podcast_files (
            id INT AUTO_INCREMENT PRIMARY KEY,
            doc_id VARCHAR(64) UNIQUE,
            file_name VARCHAR(255),
            file_size INT,
            created_at VARCHAR(50),
            modified_at VARCHAR(50),
            transcription TEXT
        )
    """)

    # related table with foreign key
    db.execute("""
        CREATE TABLE IF NOT EXISTS threat_analysis (
            id INT AUTO_INCREMENT PRIMARY KEY,
            file_id INT,
            bds_percent FLOAT,
            is_bds BOOLEAN,
            bds_threat_level VARCHAR(20),
            analyzed_at VARCHAR(50),
            FOREIGN KEY (file_id) REFERENCES podcast_files(id)
        )
    """)
```

rules:
- every table has `id INT AUTO_INCREMENT PRIMARY KEY`
- foreign keys use the auto-increment `id` from the parent table
- `doc_id` is UNIQUE but not the primary key — the auto-increment `id` is the pk
- `setup_tables()` is called once at startup in `main.py`

#### dal (data access layer)
file: `<service>/dal.py`

all sql queries live here. each function is one query. the function calls `db.query()` or `db.execute()` and returns the result. comments above each function explain the query logic.

```python
from database import db


# --- EXAMPLE QUERIES (templates — uncomment and adapt when data is available) ---


# # basic select with order by
# def get_all_files_sorted():
#     # select all files, order by file size descending
#     sql = """
#         SELECT doc_id, file_name, file_size
#         FROM podcast_files
#         ORDER BY file_size DESC
#     """.strip()
#     return db.query(sql)


# # where clause filtering
# def get_large_files(min_size):
#     # select files larger than a given size
#     sql = """
#         SELECT doc_id, file_name, file_size
#         FROM podcast_files
#         WHERE file_size > %s
#         ORDER BY file_size DESC
#     """.strip()
#     return db.query(sql, (min_size,))


# # join — combine files with their threat analysis
# def get_files_with_threats():
#     # join podcast_files to threat_analysis on file_id
#     sql = """
#         SELECT podcast_files.doc_id, podcast_files.file_name,
#                threat_analysis.bds_percent, threat_analysis.bds_threat_level
#         FROM podcast_files
#         JOIN threat_analysis ON threat_analysis.file_id = podcast_files.id
#         ORDER BY threat_analysis.bds_percent DESC
#     """.strip()
#     return db.query(sql)


# # left join — all files including those without analysis
# def get_all_files_with_optional_threats():
#     # left join so files without analysis still appear
#     sql = """
#         SELECT podcast_files.doc_id, podcast_files.file_name,
#                threat_analysis.bds_percent, threat_analysis.bds_threat_level
#         FROM podcast_files
#         LEFT JOIN threat_analysis ON threat_analysis.file_id = podcast_files.id
#         ORDER BY podcast_files.file_name
#     """.strip()
#     return db.query(sql)


# # group by with count
# def count_files_by_threat_level():
#     # count files per threat level
#     sql = """
#         SELECT threat_analysis.bds_threat_level, COUNT(podcast_files.id) AS file_count
#         FROM podcast_files
#         JOIN threat_analysis ON threat_analysis.file_id = podcast_files.id
#         GROUP BY threat_analysis.bds_threat_level
#         ORDER BY file_count DESC
#     """.strip()
#     return db.query(sql)


# # having — filter on aggregates
# def get_threat_levels_with_multiple_files():
#     # only return threat levels that have more than 1 file
#     sql = """
#         SELECT threat_analysis.bds_threat_level, COUNT(podcast_files.id) AS file_count
#         FROM podcast_files
#         JOIN threat_analysis ON threat_analysis.file_id = podcast_files.id
#         GROUP BY threat_analysis.bds_threat_level
#         HAVING COUNT(podcast_files.id) > 1
#     """.strip()
#     return db.query(sql)


# # subquery — files with above-average bds percent
# def get_above_average_threats():
#     # find files where bds_percent is above the average
#     sql = """
#         SELECT podcast_files.doc_id, podcast_files.file_name, threat_analysis.bds_percent
#         FROM podcast_files
#         JOIN threat_analysis ON threat_analysis.file_id = podcast_files.id
#         WHERE threat_analysis.bds_percent > (
#             SELECT AVG(bds_percent) FROM threat_analysis
#         )
#         ORDER BY threat_analysis.bds_percent DESC
#     """.strip()
#     return db.query(sql)


# # cte (common table expression) — rank files by danger
# def get_ranked_threats():
#     # define a cte with threat data, then select from it
#     sql = """
#         WITH threat_data AS (
#             SELECT podcast_files.doc_id, podcast_files.file_name,
#                    threat_analysis.bds_percent, threat_analysis.bds_threat_level
#             FROM podcast_files
#             JOIN threat_analysis ON threat_analysis.file_id = podcast_files.id
#         )
#         SELECT doc_id, file_name, bds_percent, bds_threat_level
#         FROM threat_data
#         WHERE bds_threat_level != 'none'
#         ORDER BY bds_percent DESC
#     """.strip()
#     return db.query(sql)


# # window function — row number ranking
# def get_files_ranked_by_size():
#     # rank files by size within each threat level
#     sql = """
#         SELECT podcast_files.doc_id, podcast_files.file_name, podcast_files.file_size,
#                threat_analysis.bds_threat_level,
#                ROW_NUMBER() OVER (
#                    PARTITION BY threat_analysis.bds_threat_level
#                    ORDER BY podcast_files.file_size DESC
#                ) AS size_rank
#         FROM podcast_files
#         JOIN threat_analysis ON threat_analysis.file_id = podcast_files.id
#     """.strip()
#     return db.query(sql)
```

#### router calling dal
file: `<service>/router.py`

the router imports dal functions and calls them. it formats the raw tuples into json-friendly dicts.

```python
from fastapi import APIRouter
from dal import get_all_files_sorted, get_files_with_threats

router = APIRouter()


# @router.get("/files/sorted")
# def files_sorted_route():
#     rows = get_all_files_sorted()
#     result = []
#     for row in rows:
#         result.append({
#             "doc_id": row[0],
#             "file_name": row[1],
#             "file_size": int(row[2])
#         })
#     return result


# @router.get("/files/with-threats")
# def files_with_threats_route():
#     rows = get_files_with_threats()
#     result = []
#     for row in rows:
#         result.append({
#             "doc_id": row[0],
#             "file_name": row[1],
#             "bds_percent": float(row[2]),
#             "bds_threat_level": row[3]
#         })
#     return result
```

rules:
- database class handles ALL connection management — dal never opens/closes connections
- dal functions contain ONLY sql queries — no connection logic, no formatting
- router handles ONLY http + response formatting — no sql, no connection logic
- `table_config.py` runs at startup to create tables
- every table has auto-increment id and foreign keys where applicable
- example queries are commented out as templates — uncomment and adapt when data is available
- one dal function = one sql query
- comments above each dal function explain the query in plain english

---

## 13 docker rules

### 13.1 per-service dockerfile
every service must have its own dockerfile inside its folder.
every dockerfile copies the shared folder.

for consumer/script services:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shared/ ./shared/
COPY <service>/ ./
CMD ["python", "main.py"]
```

for fastapi services:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shared/ ./shared/
COPY <service>/ ./
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

for streamlit services:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shared/ ./shared/
COPY <service>/ ./
CMD ["streamlit", "run", "dashboard.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

if the service needs shared data files add:
```dockerfile
COPY data/ ./data/
```

### 13.2 requirements.txt — per-service files
each service folder has its own `requirements.txt` listing only the packages that service actually uses. the dockerfile copies and installs from the service's own file.

```
file_ingestor/requirements.txt         confluent-kafka, elasticsearch
file_to_mongo_es/requirements.txt      confluent-kafka, pymongo, elasticsearch
audio_transcriber/requirements.txt     confluent-kafka, elasticsearch, SpeechRecognition
content_analyzer/requirements.txt      confluent-kafka, elasticsearch
data_gateway/requirements.txt          fastapi, uvicorn, pymongo, elasticsearch
```

the dockerfile copies its own requirements file:
```dockerfile
COPY <service>/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

a root `requirements.txt` still exists with all packages combined — used only for running tests and connection_tests locally. it is not referenced by any dockerfile.

### 13.3 docker-compose style
the compose file must follow this structure and style:

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
    ...

# +--------------------+
# |   MONGO UI (WEB)   |
# +--------------------+
  mongo-express:
    ...

#############################################################################################################
##################################+---------------------------+##############################################
##################################|     ~   CODE   ~          |##############################################
##################################+---------------------------+##############################################
#############################################################################################################

# +------------------------+
# | service_name           |
# +------------------------+
  service_name:
    build:
      context: .
      dockerfile: service_name/Dockerfile
    ...
```

rules:
- ascii art separators between infrastructure (IMAGES) and application code (CODE) sections
- each service gets a box-style comment header
- `context: .` is always the project root so COPY paths work
- `dockerfile:` points to the service-specific dockerfile
- no `command:` override — CMD is in the dockerfile
- environment variables here override `os.getenv()` defaults in code
- all services must be on the same docker network
- infrastructure services come first, each with its UI companion
- application services come after the CODE separator
- `restart: "no"` for run-once scripts
- `restart: unless-stopped` for loop services and apis
- every infrastructure service gets a UI companion when available:
  - mongo -> mongo-express
  - kafka -> kafka-ui
  - mysql -> cloudbeaver
  - redis -> redisinsight
  - elasticsearch -> kibana

**kafka image:** always use `confluentinc/cp-kafka` (not bitnami/kafka). confluent is the primary maintainer of the kafka ecosystem and the confluent-kafka python library — using the same vendor for the broker and the client avoids version compatibility issues.

```yaml
kafka:
  image: confluentinc/cp-kafka:7.8.3
  environment:
    KAFKA_NODE_ID: 1
    KAFKA_PROCESS_ROLES: broker,controller
    KAFKA_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093
    KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
    KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
    KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
    KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
    CLUSTER_ID: MkU3OEVBNTcwNTJENDM2Qk
  ports:
    - "9092:9092"
  restart: unless-stopped
```

always use the latest stable versions of all infrastructure images at time of project creation.

### 13.4 .env file for docker-compose
the `.env` file at root is only for docker-compose `${VAR}` substitution.
it contains the values that docker-compose.yml references with `${...}` syntax.

```
MONGO_DB=my_database
```

---

## 14 docstring rules

every python file must have a short simple docstring at the very top.
do not put filename comments like `# file: something.py` at the top.
the docstring is the first thing in the file — before any imports.

### 14.1 first docstring — short summary
format — three lines max, plain and simple:
```python
"""
what this file does in one sentence
gets: what it receives or reads
gives: what it produces or sends
"""
```

example for a kafka consumer service:
```python
"""
consumes file events from kafka and stores audio in mongo gridfs and metadata in elasticsearch
gets: json messages from kafka topic file-events
gives: audio binary to mongodb gridfs, metadata to elasticsearch
"""
```

example for a config file:
```python
"""
loads environment variables for the file ingestor service
gets: env vars or defaults
gives: config values to other modules
"""
```

### 14.2 second docstring — flow, variables, and strategy
immediately after the first docstring (still before imports), add a second docstring that documents the internal flow, key variables/components, and the reasoning behind important decisions in this file.

format:
```python
"""
flow:
    1. receives message from kafka with file path and metadata
    2. reads the wav file from the shared volume
    3. computes sha-256 hash of file content as doc_id
    4. stores wav binary in mongodb gridfs with doc_id
    5. indexes metadata in elasticsearch with doc_id

components:
    kafka_consumer - confluent kafka consumer, polls file-events topic
    gridfs_storage - pymongo gridfs instance, stores binary audio files
    elasticsearch_client - elasticsearch connection, indexes metadata documents
    publisher - kafka publisher, sends confirmation to file-processed topic
    config - environment variables for all connection strings and topic names

strategy:
    - sha-256 hash of file bytes is used as doc_id so any service can recompute the same id
      independently from the file content — no coordination between services needed
    - file is read into memory once and reused for both hashing and gridfs storage
      to avoid reading the file twice
    - metadata is indexed in elasticsearch before storing the binary in gridfs
      so the document exists for queries even if gridfs storage is slow
"""
```

rules:
- the flow section lists the steps in order — what happens from start to finish
- the components section lists key variables/objects and what they are in plain english
- the strategy section explains WHY key decisions were made — not what the code does, but the reasoning behind it
  - why this data structure or format was chosen
  - why this service computes something itself instead of receiving it
  - why steps are done in a specific order
  - why a specific library or approach was chosen over alternatives
- strategy is especially important for orchestrator files where design decisions are made
- for simple files (config, __init__) the second docstring can be skipped
- only include strategy points that are non-obvious — do not explain things that are self-evident from the code

### 14.3 general docstring rules
- every `.py` file gets at least the first docstring
- keep it very short and simple
- no INPUT/OUTPUT/FLOW labels — just plain english
- no uppercase section headers inside the docstring
- do not repeat the filename in the docstring

---

## 15 readme rules

every project must have a `doc/README.md` with:
- project title and one-line description
- ascii flow diagram showing the full data pipeline
- table of services with ports and descriptions
- table of infrastructure with ports
- table of message broker topics with producer and consumer columns
- quick start section with docker compose command and example curl/api calls
- project structure tree showing all folders and key files

---

## 16 service types

projects can contain four types of services:

### 16.1 run-once script
- runs once when container starts then exits
- `restart: "no"` in compose
- `CMD ["python", "main.py"]`
- example: data seeder, migration script

### 16.2 loop service (consumer)
- runs in a while True loop polling kafka or another source
- `restart: unless-stopped` in compose
- `CMD ["python", "main.py"]`
- uses the orchestrator pattern with get_message + start methods

### 16.3 fastapi service
- http api
- `restart: unless-stopped` in compose
- `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "XXXX"]`
- has `main.py` and `router.py`

### 16.4 streamlit dashboard
- web dashboard for visualization
- `restart: unless-stopped` in compose
- `CMD ["streamlit", "run", "dashboard.py", "--server.port", "8501", "--server.address", "0.0.0.0"]`
- has `dashboard.py` as the entry point


---

## PROJECT STYLE & MINDSET


# project instruction — prompt engineer role

## who you are
you are a prompt engineer.
you do not write code.
you do not build the project.
your job is to produce clear, precise prompts that a separate claude code session will execute.

## the goal
we are building educational backend projects together.
i bring you task instructions (often in hebrew).
you read them, summarize the goal in english, ask me to confirm, then produce a ready-to-paste prompt for claude code.

this week is a test week — we are learning how to work together so the prompts you produce get the desired outcome with minimal corrections.

## your workflow for each task
1. i give you task instructions
2. you read them carefully
3. you summarize the goal and ask me to confirm before producing anything
4. once i confirm, you write a clear task prompt in english
5. i paste that prompt into a new claude code chat along with the system prompt template
6. after i run it, i come back and tell you the result
7. if there were issues, we adjust the prompt approach and update the rules if needed
8. you update `project_state.md` with what was completed

## files you manage
- `rules_claude.md` — the permanent ruleset for claude code. you update it when we learn something new
- `project_state.md` — the living state tracker. you update it after every completed task
- `chat_system_prompt.md` — the template i paste into each claude code chat. you update it if the format needs to change

## what you do not do
- you do not write application code
- you do not build files or folders for the project
- you do not guess what the task wants — if unclear, ask me
- you do not produce a prompt until i confirm the summary

## key principles
- all prompts and outputs must be in english
- instructions from me may be in hebrew — you translate and summarize
- keep prompts simple and direct — match the educational tone of the project
- reference the rules file in every prompt so claude code follows them
- if a task conflicts with existing rules, flag it and ask me how to proceed
- after each task, track what worked and what needed correction so we improve over time

---

## prompt format rules

every task prompt must follow this structure in this order:

### 1. overview
a short paragraph explaining the overall goal of the task — what we are building and why.

### 2. service map
list every service involved in this task. for each service, clearly state:
- **name** — the service folder name. follow the naming convention:
  - services that only save/move data → named by flow (e.g. `file_to_mongo_es`)
  - services that transform/modify/extract data → use action words (e.g. `audio_transcriber`, `text_processor`)
- **type** — run-once / loop / fastapi / streamlit (from the rules)
- **role** — one sentence on what this service does in the system
- **gets** — what this service receives as input (kafka messages, files from a folder, api requests, env vars, etc). be specific about the source and format. if kafka — state the topic name and consumer group
- **does** — step by step, what the service does with its input. numbered list, short and clear
- **gives** — what this service produces as output and where it goes (kafka topic, mongodb collection, elasticsearch index, api response, file on disk, etc). be specific about the destination

### 3. data flow
show the full path of data through the system from start to finish.
use a simple arrow diagram like:
```
folder (wav files) -> file_ingestor -> kafka (file-events) -> file_to_mongo_es -> mongo (gridfs) + elasticsearch (podcast-metadata)
```

### 4. shared modules
list which shared modules are needed and if any new ones need to be created.

### 5. infrastructure
list all docker infrastructure services, their images, and their ui companions.
mention any special config (like single-node elasticsearch, kraft mode kafka, etc).

### 6. docker details
anything important about volumes, networks, depends_on, env vars, or container access to files/folders.
this is where we prevent issues like "service B cant access the file because its not in its container."
if multiple services consume from the same kafka topic, explicitly state each service's consumer group name.

### 7. file structure
the expected folder and file tree.

### 8. tests
what test scripts to create in `tests/` and what each one demonstrates.
for each test, state which project file's logic it is demonstrating.

### 9. connection tests
what connection test scripts to create in `connection_tests/`.
list each infrastructure dependency that needs a connection test.

### 10. demo files
if the task involves processing files (audio, images, json, csv, etc.), check if demo files are available or ask the user for them. never create dummy or fake input files — always use real files provided by the user.

### 11. other files
any remaining files — .env, .gitignore, .dockerignore, requirements.txt.
all markdown documentation files go in the `doc/` folder: README.md, run.md, project_state.md, sql docs.
run.md must always include a "local setup" section with venv creation, activation, and `pip install -r requirements.txt`. the terminal on windows is git bash (activation: `source venv/Scripts/activate`). infrastructure runs via docker-compose, python code and tests run locally against it.
`doc/` must be in `.gitignore` and `.dockerignore`.

every prompt must end with this reminder:
> **after completing all tasks above, update `doc/project_state.md`** — add the new task to the task log, add any new files to the file list, update the project structure tree, and update the detailed summary if needed.

---

## ambiguity rule

if anything in the task is open to interpretation — especially around:
- how data moves between services
- what a service has access to (files, volumes, network)
- what format data should be in
- whether something should be stored, passed, or both

**stop and ask me before writing the prompt.**
do not make assumptions. do not pick the "most likely" option.
ask, confirm, then write.

---

## minimal code principle

the goal is bare minimum code. when writing prompts:
- only describe what is strictly needed to fulfill the task
- if a prompt implies extra code (filtering, validation, safety checks) that was not explicitly requested, either remove it from the prompt or clearly mark it as optional/extra
- if claude code might interpret a prompt as requiring extra robustness, add a note like: "do not add extra filtering/validation unless described here"
- remember: anything beyond the bare minimum in the generated code must be marked with a comment block explaining what it is, why it is there, and whether it was requested or added independently (see rules section 7)

---

## code quality standards

every prompt should reinforce these standards (they are in the rules but worth reminding):

### variable naming
- all variable and parameter names must be clear and descriptive
- no shortened unclear names like `fs`, `es`, `f`, `r`, `db`
- use full names: `gridfs_storage`, `elasticsearch_client`, `file_handle`, `kafka_message`
- see rules section 3 for full details

### config class attributes
- config class attributes must use UPPERCASE names matching the env var they load
- example: `self.KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")`
- config values are constants — UPPERCASE is the correct python convention
- see rules section 8.2 for full details

### file documentation
- every python file must have two docstrings at the top (before imports):
  1. short summary — what the file does, what it gets, what it gives (3 lines max)
  2. detailed flow — three sections: `flow:` (numbered steps), `components:` (key variables), `strategy:` (why decisions were made)
- the `strategy:` section is the most important addition — it explains the reasoning behind non-obvious choices:
  - why a specific approach was chosen (e.g. sha-256 hash vs uuid for doc_id)
  - why steps are in a specific order
  - why data is stored/passed in a particular way
  - why a library was chosen over alternatives
- only document decisions that are non-obvious — skip things the code already makes clear
- see rules section 14 for exact format and examples

### logger usage
- all services use the class-based Logger from `shared/logger.py`
- import: `from shared.logger import Logger`
- usage: `Logger.get_logger(name, es_host, log_index)`
- every success → `logger.info()`, every failure → `logger.error()` with full error details
- see rules section 8.3 for the exact Logger class code

---

## prompt quality checklist

before delivering a prompt, verify:
- [ ] every service clearly states what it gets and gives
- [ ] service names follow the naming convention (save/move → flow name, transform → action name)
- [ ] data flow makes physical sense (files accessible, paths valid, containers can reach each other)
- [ ] no service reads from something it doesnt have access to
- [ ] docker volumes and mounts are explicitly described when services share files
- [ ] kafka topics are named and both producer and consumer are identified
- [ ] if multiple consumers share a topic, each has a distinct consumer group
- [ ] infrastructure dependencies are clear (depends_on)
- [ ] the prompt references the rules file
- [ ] no extra code or logic is implied beyond what the task requires
- [ ] variable names are descriptive (no short unclear abbreviations)
- [ ] config class attributes use UPPERCASE names
- [ ] each service has its own requirements.txt listing only its actual dependencies
- [ ] kafka image is confluentinc/cp-kafka (not bitnami)
- [ ] elasticsearch index is created explicitly with setup_index() at service startup
- [ ] file documentation format is specified (two docstrings per file — including strategy: section in orchestrators)


---

## PROJECT STATE TEMPLATE

You MUST fill in the template below and save it as `doc/project_state.md` in the generated project.
Update every field based on what you actually built.


# project state

this file tracks the current state of the project.
updated after every task completion.

---

## current status

| field | value |
|-------|-------|
| last updated | — |
| total tasks completed | 0 |
| total files | 0 |
| project name | (tbd) |

---

## task log

| # | date | task title | status |
|---|------|-----------|--------|
| — | — | — | — |

---

## file list

| # | file path | created in task # | description |
|---|-----------|-------------------|-------------|
| — | — | — | — |

---

## tech stack

| category | tool | purpose |
|----------|------|---------|
| — | — | — |

---

## infrastructure

| service | image | port (host:container) | ui companion |
|---------|-------|-----------------------|-------------|
| — | — | — | — |

---

## application services

| service | type | port | description |
|---------|------|------|-------------|
| — | — | — | — |

types: run-once / loop / fastapi / streamlit

---

## kafka topics

| topic | producer | consumer |
|-------|----------|----------|
| — | — | — |

---

## project structure

```
(updated after each task)
```

---

## detailed summary

(a running description of what the project does, the full data flow, and how the pieces connect — updated as the project grows)


---

## INSTRUCTION FILES

### dilemmas.md

```
# Dilemmas

## 1. Where to place README.md

**Dilemma:** The CRITICAL OPERATING RULES say "Include a README.md with clear setup and run instructions", while the permanent coding rules (section 15) say every project must have a `doc/README.md`. These two instructions point to different locations.

**Options considered:**
- Put README.md at the project root (satisfies the critical rule literally)
- Put README.md inside `doc/` folder (satisfies the permanent coding rules)
- Put README.md in both places

**Choice:** README.md is placed inside `doc/` and a short README.md is also placed at the project root pointing to `doc/README.md`.

**Why:** The permanent coding rules are explicit about `doc/README.md`. The root README serves as a pointer so anyone who opens the folder immediately knows where to look.

---

## 2. Apply fix.md immediately or separately

**Dilemma:** The project includes both `instructions.md` (build the project) and `fix.md` (add docstrings and comments). Since this is a NEW PROJECT, it is unclear whether to build first then patch, or build with all improvements from the start.

**Options considered:**
- Build the script without docstrings, then apply fix.md as a second pass
- Build the script with all docstrings and comments already included

**Choice:** Built the script with all docstrings and comments included from the start.

**Why:** Applying a fix on top of newly created code adds unnecessary steps. Since both instructions are available up front, building the final version directly is simpler and cleaner.

---

## 3. Architecture rules vs simple standalone script

**Dilemma:** The permanent coding rules describe a full multi-service backend architecture (docker-compose, shared/ folder, Kafka, Elasticsearch, etc.). The actual project is a simple standalone Python script with no external services.

**Options considered:**
- Apply all architecture rules (create docker-compose, shared/, services/ structure)
- Apply only the rules that are relevant to a single-script project

**Choice:** Applied only relevant rules (file docstrings, comment style, variable naming, doc/ folder, dilemmas.md, project_state.md). Skipped Docker, Kafka, Elasticsearch, shared/ folder, and service structure entirely.

**Why:** The instructions.md explicitly says "Python standard library only" and "no pip installs". The architecture rules are designed for multi-service backend systems. Forcing that structure onto a single stdlib script would violate the "keep it simple and educational" principle.

```

### doc\project_state.md

```
# project state

this file tracks the current state of the project.
updated after every task completion.

---

## current status

| field | value |
|-------|-------|
| last updated | 2026-03-10 |
| total tasks completed | 2 |
| total files | 7 |
| project name | student grade averager |

---

## task log

| # | date | task title | status |
|---|------|-----------|--------|
| 1 | 2026-03-10 | build student grade averager script | completed |
| 2 | 2026-03-10 | add docstrings and comments to grade_averager.py | completed |

---

## file list

| # | file path | created in task # | description |
|---|-----------|-------------------|-------------|
| 1 | grade_averager.py | 1 | main script — reads json, calculates averages, prints report |
| 2 | students.json | 1 | input data — four students with subject grades |
| 3 | requirements.txt | 1 | empty — stdlib only, no pip installs |
| 4 | dilemmas.md | 1 | documents decisions made during autonomous generation |
| 5 | doc/README.md | 1 | project overview and quick start |
| 6 | doc/run.md | 1 | local setup and run instructions |
| 7 | doc/project_state.md | 1 | this file — project state tracker |

---

## tech stack

| category | tool | purpose |
|----------|------|---------|
| language | python 3.6+ | application code |
| stdlib | json | parse students.json |
| stdlib | os | locate students.json relative to script |

---

## infrastructure

| service | image | port (host:container) | ui companion |
|---------|-------|-----------------------|-------------|
| — | — | — | — |

no infrastructure services — stdlib only, runs locally

---

## application services

| service | type | port | description |
|---------|------|------|-------------|
| grade_averager.py | run-once script | — | reads student grades json and prints summary |

---

## kafka topics

| topic | producer | consumer |
|-------|----------|----------|
| — | — | — |

no message broker — simple standalone script

---

## project structure

```
project_1/
├── grade_averager.py
├── students.json
├── requirements.txt
├── dilemmas.md
└── doc/
    ├── README.md
    ├── run.md
    └── project_state.md
```

---

## detailed summary

this project is a simple standalone python script that reads student grade data from a local json file and prints a formatted summary to the terminal.

the script has four functions:
- `load_students()` — opens and parses students.json
- `calculate_average()` — computes the mean of a grades dict, returns none if empty
- `format_student_line()` — formats one output line per student
- `print_report()` — loops through all students, prints individual lines, then prints class average and top student

the data flows from students.json through the python functions and out to the terminal. no external services, no network calls, no pip dependencies.

task 2 (fix.md) added docstrings to every function and visible comments above logical sections of the main script, without changing any logic.

```

### doc\README.md

```
# Student Grade Averager

A simple Python script that reads student data from a JSON file and prints a formatted grade summary to the terminal.

## Data Flow

```
students.json  ->  grade_averager.py  ->  terminal output
```

## What It Does

1. Reads `students.json` from the same folder
2. Calculates each student's average grade across all their subjects
3. Prints each student's name and average (or "no grades" if they have none)
4. Prints the overall class average and the top student

## Example Output

```
Alice    — average: 87.3
Bob      — average: 74.0
Carol    — average: 91.7
David    — no grades

Class average: 84.3
Top student: Carol (91.7)
```

## Project Structure

```
project_1/
├── grade_averager.py   # main script
├── students.json       # input data
├── requirements.txt    # no external dependencies
├── dilemmas.md         # decisions made during generation
└── doc/
    ├── README.md       # this file
    ├── run.md          # how to run the project
    └── project_state.md
```

## Setup and Run

No installation required — uses Python standard library only.

```bash
python grade_averager.py
```

See `doc/run.md` for full setup instructions.

```

### doc\run.md

```
# How to Run

## Local Setup

This project uses Python standard library only — no pip installs are needed.

### 1. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
```

### 2. Activate the virtual environment

On Windows with Git Bash:

```bash
source venv/Scripts/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The requirements file is empty — this step has no effect but is included for consistency.

### 4. Run the script

```bash
python grade_averager.py
```

### Expected output

```
Alice    — average: 87.3
Bob      — average: 74.0
Carol    — average: 91.7
David    — no grades

Class average: 84.3
Top student: Carol (91.7)
```

## Notes

- The script reads `students.json` from the same folder automatically
- No internet connection, no Docker, no services required
- Works with Python 3.6 and above

```

### fix.md

```
# Fix Request

## What I Want Changed

Please add a docstring to every function in `grade_averager.py` explaining:
- What the function does
- What it receives as input
- What it returns

Also add a short comment above each logical section of the main script explaining what that block of code is doing.

Do not change any of the actual logic — only add documentation.

```

### instructions.md

```
# Project: Student Grade Averager

## Overview
Build a simple Python script that reads student data from a JSON file and prints a grade summary to the terminal.

## Files to Create
- `grade_averager.py` — the main script
- `students.json` — the data file
- `requirements.txt` — empty (stdlib only)

## What the Script Does
1. Opens `students.json` from the same folder
2. For each student, calculates their average grade across all subjects
3. Prints a report like this:

```
Alice    — average: 87.3
Bob      — average: 74.0
Carol    — average: 91.7
David    — no grades

Class average: 84.3
Top student: Carol (91.7)
```

## students.json Content
```json
[
  { "name": "Alice",  "grades": { "math": 90, "english": 85, "science": 87 } },
  { "name": "Bob",    "grades": { "math": 70, "english": 78, "science": 74 } },
  { "name": "Carol",  "grades": { "math": 95, "english": 88, "science": 92 } },
  { "name": "David",  "grades": {} }
]
```

## Requirements
- Python standard library only (no pip installs)
- Handle a student with no grades — print "no grades" for them
- Keep the code simple and easy to read

```

### requirements.txt

```
# no external dependencies — stdlib only

```

---

## CODE FILES PROVIDED

### grade_averager.py
```
"""
reads student grade data from a json file and prints a grade summary report
gets: students.json file with student names and subject grades
gives: formatted grade report printed to terminal
"""

"""
flow:
    1. reads students.json from the same directory as the script
    2. for each student, calculates the average of their grades
    3. prints each student's name and average (or "no grades" if empty)
    4. calculates the class average across all students who have grades
    5. finds and prints the top student with the highest average

components:
    student_list - list of student dicts loaded from students.json
    averages - dict mapping student name to their calculated average
    class_average - the mean of all individual student averages who have grades

strategy:
    - students with no grades are skipped when calculating class average
      so they do not cause a division by zero or skew the result
    - averages is built as a dict keyed by name so finding the max is
      a single call to max() without a second loop over the list
    - the script uses os.path to locate students.json relative to the script
      so it works from any working directory, not just the project folder
"""

import json
import os


def load_students(file_path):
    """
    reads the students json file and returns the list of student records
    receives: file_path — the full path to the json file as a string
    returns: a list of dicts, each with a name key and a grades dict
    """
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def calculate_average(grades):
    """
    calculates the numeric average of a grades dictionary
    receives: grades — a dict mapping subject names to numeric grade values
    returns: the average rounded to one decimal place, or None if grades is empty
    """
    if not grades:
        return None
    total = sum(grades.values())
    return round(total / len(grades), 1)


def format_student_line(student_name, average):
    """
    formats one line of the grade report for a single student
    receives: student_name — the student's name as a string
              average — a float with their average grade, or None if no grades
    returns: a formatted string ready to print to the terminal
    """
    if average is None:
        return f"{student_name:<8} — no grades"
    return f"{student_name:<8} — average: {average}"


def print_report(student_list):
    """
    builds and prints the full grade report for all students in the list
    receives: student_list — a list of student dicts with name and grades fields
    returns: nothing, prints the report directly to the terminal
    """
    averages = {}

    # print each student's individual result
    for student in student_list:
        student_name = student["name"]
        grades = student["grades"]
        average = calculate_average(grades)
        if average is not None:
            averages[student_name] = average
        print(format_student_line(student_name, average))

    print()

    # calculate and print the overall class average
    if averages:
        class_average = round(sum(averages.values()) / len(averages), 1)
        print(f"Class average: {class_average}")

        # find and print the student with the highest average
        top_student_name = max(averages, key=averages.get)
        top_average = averages[top_student_name]
        print(f"Top student: {top_student_name} ({top_average})")


# locate students.json in the same folder as this script
script_directory = os.path.dirname(os.path.abspath(__file__))
students_file_path = os.path.join(script_directory, "students.json")

# load the student data from the json file
student_list = load_students(students_file_path)

# print the full grade report
print_report(student_list)

```

---

## DATA FILES

### students.json (287 bytes — inline preview)
```
[
  { "name": "Alice",  "grades": { "math": 90, "english": 85, "science": 87 } },
  { "name": "Bob",    "grades": { "math": 70, "english": 78, "science": 74 } },
  { "name": "Carol",  "grades": { "math": 95, "english": 88, "science": 92 } },
  { "name": "David",  "grades": {} }
]

```

---

## FINAL CHECKLIST

Before finishing, verify:
- [ ] All requested features are fully implemented (no TODOs)
- [ ] `README.md` exists with setup and run instructions
- [ ] All dependency files exist (requirements.txt, package.json, etc.)
- [ ] `dilemmas.md` exists (even if it says "No dilemmas encountered")
- [ ] `doc/project_state.md` is filled in with all fields completed
- [ ] All code follows the permanent coding rules above
- [ ] All code is syntactically valid and runnable
- [ ] Error handling covers obvious failure cases

**Start now. Generate the complete project.**
