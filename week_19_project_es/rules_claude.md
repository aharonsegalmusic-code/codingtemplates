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
