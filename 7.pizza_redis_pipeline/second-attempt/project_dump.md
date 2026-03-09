# PROJECT TREE

```
.claude/ [subfolders: 0, files: 1, total files: 1]
    settings.local.json
.env.local
.env.prod
api/ [subfolders: 2, files: 5, total files: 21]
    __init__.py
    __pycache__/ [subfolders: 0, files: 4, total files: 4]
        __init__.cpython-314.pyc
        api.cpython-314.pyc
        health_routes.cpython-314.pyc
        router.cpython-314.pyc
    api.py
    connection/ [subfolders: 1, files: 6, total files: 12]
        __init__.py
        __pycache__/ [subfolders: 0, files: 6, total files: 6]
            __init__.cpython-314.pyc
            kafka_connection.cpython-314.pyc
            kafka_connection_producer.cpython-314.pyc
            mongo_connection.cpython-314.pyc
            mysql_connection.cpython-314.pyc
            redis_connection.cpython-314.pyc
        kafka_connection_producer.py
        mongo_connection.py
        mysql_connection.py
        redis_connection.py
        test_connections.py
    health_routes.py
    router.py
    test.py
docker-compose.yml
enricher/ [subfolders: 1, files: 1, total files: 11]
    connection/ [subfolders: 1, files: 4, total files: 10]
        __init__.py
        __pycache__/ [subfolders: 0, files: 6, total files: 6]
            __init__.cpython-314.pyc
            kafka_connection.cpython-314.pyc
            kafka_connection_producer.cpython-314.pyc
            mongo_connection.cpython-314.pyc
            mysql_connection.cpython-314.pyc
            redis_connection.cpython-314.pyc
        kafka_connection_consumer.py
        mongo_connection.py
        redis_connection.py
    enricher_consumer.py
kitchen/ [subfolders: 2, files: 1, total files: 13]
    __pycache__/ [subfolders: 0, files: 1, total files: 1]
        kitchen_worker.cpython-314.pyc
    connection/ [subfolders: 1, files: 4, total files: 11]
        __init__.py
        __pycache__/ [subfolders: 0, files: 7, total files: 7]
            __init__.cpython-314.pyc
            kafka_connection.cpython-314.pyc
            kafka_connection_consumer.cpython-314.pyc
            kafka_connection_producer.cpython-314.pyc
            mongo_connection.cpython-314.pyc
            mysql_connection.cpython-314.pyc
            redis_connection.cpython-314.pyc
        kafka_connection_consumer.py
        mongo_connection.py
        redis_connection.py
    kitchen_worker.py
requirements.txt
STATE.MD
test.py
text_processor/ [subfolders: 2, files: 3, total files: 14]
    __init__.py
    __pycache__/ [subfolders: 0, files: 3, total files: 3]
        __init__.cpython-314.pyc
        clean_preprocessor.cpython-314.pyc
        text_worker.cpython-314.pyc
    clean_preprocessor.py
    connection/ [subfolders: 1, files: 4, total files: 8]
        __init__.py
        __pycache__/ [subfolders: 0, files: 4, total files: 4]
            __init__.cpython-314.pyc
            kafka_connection_consumer.cpython-314.pyc
            kafka_connection_producer.cpython-314.pyc
            mongo_connection.cpython-314.pyc
        kafka_connection_consumer.py
        kafka_connection_producer.py
        mongo_connection.py
    text_worker.py
```

# PROJECT STATS

- Total folders: 16
- Total files  : 66

## File types

| Extension | Files | Lines (utf-8 text only) |
|---|---:|---:|
| `.json` | 1 | 8 |
| `.local` | 1 | 23 |
| `.MD` | 1 | 18 |
| `.prod` | 1 | 26 |
| `.py` | 29 | 964 |
| `.pyc` | 31 | 0 |
| `.txt` | 1 | 14 |
| `.yml` | 1 | 147 |

---

# FILE CONTENTS

## .claude/settings.local.json

```json
{
  "permissions": {
    "allow": [
      "Bash(python:*)"
    ]
  }
}
```

## .env.local

```
MONGO_URI=mongodb://127.0.0.1:27017/
MONGO_DB=pizza_mongo
MONGO_COLLECTION=orders_mongo
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_ROOT_PASSWORD=root_pwd
MYSQL_DATABASE=pizza_mysql
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=
KAFKA_BOOTSTRAP_SERVERS=127.0.0.1:9092
TOPIC_ORDERS=pizza_orders
TOPIC_CLEAN_INST=cleaned-instructions
KAFKA_GROUP_ID_KITCHEN=pizza-kitchen
KAFKA_GROUP_ID_ENRICHER=pizza-enricher
KAFKA_GROUP_ID_TEXT=pizza-text
CLUSTER_ID=Mf_-9PUJQnCI6eQZzgFTlg
KAFKA_UI_URL=http://127.0.0.1:18080
MONGO_EXPRESS_URL=http://127.0.0.1:18081
CLOUDBEAVER_URL=http://127.0.0.1:8978
REDISINSIGHT_URL=http://127.0.0.1:5540
```

## .env.prod

```

MONGO_URI=mongodb://127.0.0.1:27017/
MONGO_DB=pizza_mongo
MONGO_COLLECTION=orders_mongo
ME_CONFIG_MONGODB_ENABLE_LOGIN=false
ME_CONFIG_BASICAUTH=false
ME_CONFIG_MONGODB_SERVER=mongo
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_ROOT_PASSWORD=root_pwd
MYSQL_DATABASE=pizza_mysql
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=
KAFKA_BOOTSTRAP_SERVERS=kafka:29092
TOPIC_ORDERS=pizza_orders
TOPIC_CLEAN_INST=cleaned-instructions
KAFKA_GROUP_ID_KITCHEN=pizza-kitchen
KAFKA_GROUP_ID_TEXT=pizza-text
CLUSTER_ID=Mf_-9PUJQnCI6eQZzgFTlg
KAFKA_UI_URL=http://127.0.0.1:18080
MONGO_EXPRESS_URL=http://127.0.0.1:18081
CLOUDBEAVER_URL=http://127.0.0.1:8978
REDISINSIGHT_URL=http://127.0.0.1:5540
```

## STATE.MD

```markdown
API-> 
    """
gets orders from json
    adds status field
    set ot to "PREPARING"
    inserts to mogno
    sends to kafka 
    to topic-pizza-orders
"""

NEXT

text-processor
"""



```

## api/__init__.py

```python

```

## api/__pycache__/__init__.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## api/__pycache__/api.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## api/__pycache__/health_routes.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## api/__pycache__/router.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## api/api.py

```python
"""
gets orders from json
    adds status field
    set ot to "PREPARING"
    inserts to mogno

"""

from fastapi import FastAPI

from .router import router
from .health_routes import health_router

# uvicorn api.api:app --reload

app = FastAPI(
    title="PIZZA ORDER ;)",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    print("Application starting...")


# main routes
app.include_router(
    router,
    prefix="/api",
    tags=["start_data"]
)

# health check routes
app.include_router(
    health_router,
    prefix="/api",
    tags=["health"]
)


@app.get("/")
async def root():
    return {"message": "App is running"}
```

## api/connection/__init__.py

```python

```

## api/connection/__pycache__/__init__.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## api/connection/__pycache__/kafka_connection.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## api/connection/__pycache__/kafka_connection_producer.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## api/connection/__pycache__/mongo_connection.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## api/connection/__pycache__/mysql_connection.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## api/connection/__pycache__/redis_connection.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## api/connection/kafka_connection_producer.py

```python
from confluent_kafka import Producer
import json
from typing import Callable
from dotenv import dotenv_values


ENV = dotenv_values(".env.local")

KAFKA_BOOTSTRAP_SERVERS = ENV.get("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")
TOPIC_ORDERS = ENV.get("TOPIC_ORDERS", "pizza_orders")


class KafkaProducerClient:
    def __init__(self, bootstrap_servers: str):
        self.producer = Producer({"bootstrap.servers": bootstrap_servers})

    def send(self, topic: str, value: bytes):
        self.producer.produce(topic=topic, value=value)

    def flush(self):
        self.producer.flush()

producer = KafkaProducerClient(KAFKA_BOOTSTRAP_SERVERS)
```

## api/connection/mongo_connection.py

```python
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

# --- Config ---
ENV = dotenv_values(".env.local")
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

## api/connection/mysql_connection.py

```python
from dotenv import dotenv_values
import mysql.connector

ENV = dotenv_values(".env.local")

MYSQL_HOST = ENV.get("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(ENV.get("MYSQL_PORT", "3306"))
MYSQL_USER = ENV.get("MYSQL_USER", "root")
MYSQL_PASSWORD = ENV.get("MYSQL_ROOT_PASSWORD", "root_pwd")
MYSQL_DB = ENV.get("MYSQL_DATABASE", "pizza_mysql")


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

## api/connection/redis_connection.py

```python
from dotenv import dotenv_values
import redis

ENV = dotenv_values(".env.local")

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

## api/connection/test_connections.py

```python
from mysql_connection import get_mysql_connection
from redis_connection import r
from mongo_connection import mongo
from kafka_connection_producer import producer


def test_mysql():
    try:
        conn = get_mysql_connection()
        conn.close()
        print("MySQL: OK")
    except Exception as e:
        print(f"MySQL: FAIL - {e}")


def test_redis():
    try:
        r.ping()
        print("Redis: OK")
    except Exception as e:
        print(f"Redis: FAIL - {e}")


def test_mongo():
    try:
        mongo.client.admin.command("ping")
        print("Mongo: OK")
    except Exception as e:
        print(f"Mongo: FAIL - {e}")


def test_kafka():
    try:
        producer.producer.list_topics(timeout=5)
        print("Kafka: OK")
    except Exception as e:
        print(f"Kafka: FAIL - {e}")


if __name__ == "__main__":
    test_mysql()
    test_redis()
    test_mongo()
    test_kafka()
```

## api/health_routes.py

```python
from fastapi import APIRouter
from .connection.mongo_connection import mongo
from .connection.redis_connection import get_redis_client
from .connection.kafka_connection_producer import producer
from .connection.mysql_connection import get_mysql_connection

health_router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@health_router.get("/api")
def ping_api():
    return {"status": "ok", "service": "api"}

@health_router.get("/mongo")
def ping_mongo():
    try:
        collections = mongo.db.list_collection_names()
        if not collections:
            return {"status": "ok", "service": "mongo", "message": "connected but no collections yet"}
        return {"status": "ok", "service": "mongo", "collections": collections}
    except Exception as e:
        return {"status": "error", "service": "mongo", "message": str(e)}

@health_router.get("/redis")
def ping_redis():
    try:
        r = get_redis_client()
        r.ping()
        return {"status": "ok", "service": "redis"}
    except Exception as e:
        return {"status": "error", "service": "redis", "message": str(e)}


@health_router.get("/kafka")
def ping_kafka():
    try:
        producer 
        return {"status": "ok", "service": "kafka"}
    except Exception as e:
        return {"status": "error", "service": "kafka", "message": str(e)}


@health_router.get("/mysql")
def ping_mysql():
    try:
        conn = get_mysql_connection()
        conn.ping(reconnect=True)
        conn.close()
        return {"status": "ok", "service": "mysql"}
    except Exception as e:
        return {"status": "error", "service": "mysql", "message": str(e)}
```

## api/router.py

```python
# app/routers/public.py
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from typing import List
import json
from .connection.kafka_connection_producer import producer

from .connection.mongo_connection import mongo
from .connection.redis_connection import r

from dotenv import dotenv_values


ENV = dotenv_values(".env.local")

TOPIC_ORDERS = ENV.get("TOPIC_ORDERS", "pizza_orders")

router = APIRouter(
    prefix="/file_data",
    tags=["file"],
)

# =============================
#   +-----------------------+
#   |    PYDANTIC MODEL     |  
#   +-----------------------+

class Order(BaseModel):
    order_id: str
    pizza_type: str
    size: str
    quantity: int
    is_delivery: bool = False
    special_instructions: str = ""
    status: str = "PREPARING"


# =============================
#   +-----------------------+
#   |     HELPERS           |  
#   +-----------------------+

def mongo_send(data):
    """
    for each record add "status" field 
    set it to "PREPARING"
    insert one by one into mongo
    """
    collection = mongo.collection("pizza_orders")
    for order in data:
        current = Order(**order)
        collection.insert_one(current.model_dump())
        
    return {"count": len(data)}


def kafka_send(data):
    """
    send to kafka orders on by one 
    """
    for order in data:
        current = Order(**order)
        value = json.dumps(current.model_dump()).encode('utf-8')
        # send is the class function that calls produce()
        producer.send(TOPIC_ORDERS, value)
        producer.flush()  

    return {"count": len(data)}


def redis_check(order_id: str):
    """
    check if id in redis
    if is -> return it
    else -> extract from mongo and enter to redis and return it
    """

    redis_order = r.get(order_id)
    # if in redis
    if redis_order is not None:
        # convert redis(bits) to json
        redis_order = json.loads(redis_order)
        redis_order["source"] = "redis"
        return redis_order

    # if not in redis
    collection = mongo.collection("pizza_orders")
    mongo_order = collection.find_one({"order_id": order_id}, {"_id": 0})
    
    r.set(order_id, json.dumps(mongo_order), ex=60) # save in redis for 60 seconds
    # in response add source field
    mongo_order["source"] = "mongodb"
    return mongo_order


# =============================
#   +-----------------------+
#   |    ROUTES             |  
#   +-----------------------+

@router.post("/uploadfile")
def post_file(file: UploadFile = File(...)):
    data = json.loads(file.file.read())

    mongo_response = mongo_send(data)
    kafka_response = kafka_send(data)
    
    return {"mongo response": mongo_response,
            "kafka response" : kafka_response}

@router.get("/order/{order_id}")
def get_by_id(order_id:str):
    order = redis_check(order_id)
    return order
```

## api/test.py

```python
import json
from pydantic import BaseModel

# Open the file in read mode ('r') using a context manager
with open('data\pizza_orders.json', 'r') as file:
    # Parse the JSON data from the file object into a Python dictionary/list
    data = json.load(file)
    
class Order(BaseModel):
    order_id: str
    size: str
    quantity: int 
    is_delivery: bool = False
    special_instructions: str = ""
    status: str = "PREPARING"

for order in data:
    current = Order(**order)
    print("==========")
    print(current)
    break
```

## docker-compose.yml

```yaml
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
# |       MYSQL        |
# +--------------------+
  mysql:
    image: mysql:8.0
    restart: unless-stopped
    ports:
      - "3306:3306" # TODO change if port 3306 is already used
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
    volumes:
      - mysql_data:/var/lib/mysql
      - ./mysql-init:/docker-entrypoint-initdb.d:ro # NOTE: creates a mysql_native_password user so CloudBeaver/DBeaver won't hit "Public Key Retrieval is not allowed"
    networks:
      - app-network

# +--------------------+
# |   SQL UI (WEB)     |
# +--------------------+
  cloudbeaver:
    image: dbeaver/cloudbeaver:latest
    restart: unless-stopped
    ports:
      - "8978:8978" # TODO change if port 8978 is already used
    volumes:
      - cloudbeaver_data:/opt/cloudbeaver/workspace
    depends_on:
      - mysql
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
# |       REDIS        |
# +--------------------+
  redis:
    image: redis:7
    restart: unless-stopped
    ports:
      - "6379:6379" # TODO change if port 6379 is already used
    volumes:
      - redis_data:/data
    networks:
      - app-network

# +--------------------+
# |     REDIS UI       |
# +--------------------+
  redisinsight:
    image: redis/redisinsight:latest
    restart: unless-stopped
    ports:
      - "5540:5540" # TODO change if port 5540 is already used
    depends_on:
      - redis
    networks:
      - app-network

volumes:
  mongo_data:
  mysql_data:
  redis_data:
  cloudbeaver_data:

networks:
  app-network:
    driver: bridge
```

## enricher/connection/__init__.py

```python

```

## enricher/connection/__pycache__/__init__.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## enricher/connection/__pycache__/kafka_connection.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## enricher/connection/__pycache__/kafka_connection_producer.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## enricher/connection/__pycache__/mongo_connection.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## enricher/connection/__pycache__/mysql_connection.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## enricher/connection/__pycache__/redis_connection.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## enricher/connection/kafka_connection_consumer.py

```python
from confluent_kafka import Consumer
from dotenv import dotenv_values


ENV = dotenv_values(".env.local")

KAFKA_BOOTSTRAP_SERVERS = ENV.get("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")
TOPIC_CLEAN_INST = ENV.get("TOPIC_CLEAN_INST", "cleaned-instructions")
KAFKA_GROUP_ID_ENRICHER = ENV.get("KAFKA_GROUP_ID_ENRICHER", "pizza-enricher")


class KafkaConsumerClient:
    def __init__(self, bootstrap_servers: str, group_id: str):
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })

    def subscribe(self, topic: str):
        self.consumer.subscribe([topic])

    def poll(self, timeout: float = 1.0):
        return self.consumer.poll(timeout)

    def close(self):
        self.consumer.close()

consumer = KafkaConsumerClient(KAFKA_BOOTSTRAP_SERVERS,KAFKA_GROUP_ID_ENRICHER )
```

## enricher/connection/mongo_connection.py

```python
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

# --- Config ---
ENV = dotenv_values(".env.local")
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

## enricher/connection/redis_connection.py

```python
from dotenv import dotenv_values
import redis

ENV = dotenv_values(".env.local")

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

## enricher/enricher_consumer.py

```python
from .connection.kafka_connection_consumer import consumer
from .connection.mongo_connection import mongo
from .connection.redis_connection import r
import json


from dotenv import dotenv_values
ENV = dotenv_values(".env.local")
TOPIC_CLEAN_INST = ENV.get("TOPIC_CLEAN_INST", "cleaned-instructions")

collection = mongo.collection("pizza_orders")
consumer.subscribe(TOPIC_CLEAN_INST)

with open('data\pizza_analysis_lists.json', 'r') as file:
    pizza_analysis_lists = json.load(file)

# SET based on criteria to BURNT
def analyze(pizza_type):
    pizza = {"pizza_type" : pizza_type,
            "hit" : False,
            "non_kosher" : False,
            "is_meat" : False,
            "is_dairy" : True,
            "is_kosher" : True,
            "allergens" : False
            }

    # step 1 -> NOT KOSHER
    if any(pizza_type in pizza_analysis_lists[key] for key in ["forbidden_non_kosher"]):
        pizza["non_kosher"] = True
        pizza["hit"] = True
        pizza["is_kosher"] = False

    # step 1 
    if any(pizza_type in pizza_analysis_lists[key] for key in ["common_allergens"]):
        pizza["allergens"] = True

    # step 1 
    if any(pizza_type in pizza_analysis_lists[key] for key in ["dairy_ingredients"]):
        pizza["hit"] = True

    # step 1 
    if any(pizza_type in pizza_analysis_lists[key] for key in ["meat_ingredients"]):
        pizza["hit"] = True
        pizza["is_meat"] = True

    if pizza["is_dairy"] and pizza["is_meat"]:
        pizza["is_kosher"] = False  

    return pizza
    

def enricher_consumer():
    """
    listens to kafka 
    for order_id
    checks if kosher in 2 ways
        1: checks in redis 
            if not 
        2: runs analyze()
            gets the pizza is kosher params
    returns dict 
        key: pizza_type
        value: kosher params dict
    """

    print("running")
    try:
        while True:
            order = consumer.poll(1.0) 
            if order is None: continue
            if order.error():
                print(f"enricher_consumer error: {order.error()}")
                continue

            order = json.loads(order.value())
            order_id = order["order_id"]

            #start analysis
            pizza_type = order["pizza_type"]
            # check if in redis
            redis_kosher = r.get(pizza_type)
            if not redis_kosher:
                pizza = analyze(order_id)
                redis_order= r.set(pizza_type, pizza)
                
            else:
                # update in mongo as BURNT
                collection.update_one(
                {"order_id": order_id},
                {"$set": {"status": "Burnt"}},
                )           


    finally:
        consumer.close()


enricher_consumer()

# python -m enricher_consumer.enricher_consumer_worker
```

## kitchen/__pycache__/kitchen_worker.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## kitchen/connection/__init__.py

```python

```

## kitchen/connection/__pycache__/__init__.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## kitchen/connection/__pycache__/kafka_connection.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## kitchen/connection/__pycache__/kafka_connection_consumer.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## kitchen/connection/__pycache__/kafka_connection_producer.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## kitchen/connection/__pycache__/mongo_connection.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## kitchen/connection/__pycache__/mysql_connection.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## kitchen/connection/__pycache__/redis_connection.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## kitchen/connection/kafka_connection_consumer.py

```python
from confluent_kafka import Consumer
from dotenv import dotenv_values


ENV = dotenv_values(".env.local")

KAFKA_BOOTSTRAP_SERVERS = ENV.get("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")
TOPIC_ORDERS = ENV.get("TOPIC_ORDERS", "pizza_orders")
KAFKA_GROUP_ID_KITCHEN = ENV.get("KAFKA_GROUP_ID_KITCHEN", "pizza-kitchen")


class KafkaConsumerClient:
    def __init__(self, bootstrap_servers: str, group_id: str):
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })

    def subscribe(self, topic: str):
        self.consumer.subscribe([topic])

    def poll(self, timeout: float = 1.0):
        return self.consumer.poll(timeout)

    def close(self):
        self.consumer.close()

consumer = KafkaConsumerClient(KAFKA_BOOTSTRAP_SERVERS,KAFKA_GROUP_ID_KITCHEN)

```

## kitchen/connection/mongo_connection.py

```python
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

# --- Config ---
ENV = dotenv_values(".env.local")
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

## kitchen/connection/redis_connection.py

```python
from dotenv import dotenv_values
import redis

ENV = dotenv_values(".env.local")

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

## kitchen/kitchen_worker.py

```python
from .connection.kafka_connection_consumer import consumer
from .connection.mongo_connection import mongo
from .connection.redis_connection import r
import json
import time

from dotenv import dotenv_values
ENV = dotenv_values(".env.local")
TOPIC_ORDERS = ENV.get("TOPIC_ORDERS", "pizza_orders")

collection = mongo.collection("pizza_orders")
consumer.subscribe(TOPIC_ORDERS)


def kitchen():
    print("running")
    try:
        while True:
            order = consumer.poll(1.0) 
            if order is None: continue
            if order.error():
                print(f"kitchen error: {order.error()}")
                continue

            order = json.loads(order.value())
            order_id = order["order_id"]
            print(type(order))
            print(order)


            # sleep to see in enricher makes it BURNT
            time.sleep(15.0)

            # this is can be seen as redundant but its for validation
            if order["status"] != "BURNT":
                collection.update_one(
                {"order_id": order_id},
                {"$set": {"status": "DELIVERED"}},
                )

            r.delete(order_id)

    finally:
        consumer.close()


kitchen()

# python -m kitchen.kitchen_worker
```

## requirements.txt

```
certifi==2026.1.4
charset-normalizer==3.4.4
confluent-kafka==2.13.0
dnspython==2.8.0
idna==3.11
mysql-connector-python==9.6.0
psutil==7.2.2
pymongo==4.16.0
python-dotenv==1.2.1
PyYAML==6.0.3
redis==7.1.1
requests==2.32.5
urllib3==2.6.3
```

## test.py

```python
dic = {
  "common_allergens": [
    "milk",
    "dairy",
    "wheat",
    "gluten",
    "eggs",
    "soy",
    "fish",
    "shellfish",
    "shrimp",
    "clams",
    "tree nuts",
    "peanuts",
    "pine nuts",
    "walnuts",
    "sesame",
    "mustard",
    "celery",
    "sulfites"
  ],
  "forbidden_non_kosher": [
    "pork",
    "ham",
    "bacon",
    "pepperoni",
    "prosciutto",
    "salami",
    "shrimp",
    "clams",
    "lobster",
    "seafood",
    "shellfish",
    "pancetta",
    "lard"
  ],
  "meat_ingredients": [
    "chicken",
    "beef",
    "steak",
    "meatball",
    "sausage",
    "pepperoni",
    "ham",
    "bacon",
    "prosciutto",
    "salami",
    "pork",
    "meat",
    "pancetta",
    "sirloin",
    "ribeye"
  ],
  "dairy_ingredients": [
    "cheese",
    "mozzarella",
    "parmesan",
    "ricotta",
    "feta",
    "gorgonzola",
    "provolone",
    "cheddar",
    "butter",
    "cream",
    "alfredo",
    "milk",
    "dairy",
    "goat cheese"
  ]
}

pizza_type = "cheese"

pizza = {"pizza_type" : pizza_type,
         "hit" : False,
         "is_meat" : False,
         "is_dairy" : True,
         "is_kosher" : True
         }

# step 1 -> NOT KOSHER
if any(pizza_type in dic[key] for key in ["forbidden_non_kosher"]):
    pizza["hit"] = True
    pizza["is_kosher"] = False

# step 1 
if any(pizza_type in dic[key] for key in ["dairy_ingredients"]):
    pizza["hit"] = True

# step 1 
if any(pizza_type in dic[key] for key in ["meat_ingredients"]):
    pizza["hit"] = True
    pizza["is_meat"] = True

if pizza["is_dairy"] and pizza["is_meat"]:
    pizza["is_kosher"] = False  

burn = not pizza["is_kosher"]
```

## text_processor/__init__.py

```python

```

## text_processor/__pycache__/__init__.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## text_processor/__pycache__/clean_preprocessor.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## text_processor/__pycache__/text_worker.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## text_processor/clean_preprocessor.py

```python
from .connection.mongo_connection import mongo
from .connection.kafka_connection_producer import producer
import json
import re

from dotenv import dotenv_values
ENV = dotenv_values(".env.local")

TOPIC_CLEAN_INST = ENV.get("TOPIC_CLEAN_INST", "cleaned-instructions")

collection = mongo.collection("pizza_orders")

def post_to_kafka_clean(data):
    pass

def prep_extractor(pizza_type):
    with open('data/pizza_prep.json', 'r') as file:
        prep = json.load(file)

    for pizza_name, instructions in prep.items():
        if pizza_type in pizza_name:
            return instructions
    return "No prep instructions available"


def clean_instructions(order,clean_text):
    """
    1. get special_instructions and prep method from pizza_prep.json
    2. clean both texts: remove punctuation, convert to UPPERCASE
    3. update mongo with cleaned texts
    """
    pizza_type = order["pizza_type"]
    prep_text = prep_extractor(pizza_type)

    cleaned_prep = re.sub(r"[@#?$!().,]", "", prep_text.upper())

    new_cleaned = {
        "order_id" : order["order_id"],
        "pizza_type" : pizza_type,
        "special_instructions" : clean_text,
        "cleaned_prep" :cleaned_prep
    }

    # send to kafka 
    value = json.dumps(new_cleaned).encode('utf-8')
    # send is the class function that calls produce()
    producer.send(TOPIC_CLEAN_INST, value)
    producer.flush()  
    return 
```

## text_processor/connection/__init__.py

```python

```

## text_processor/connection/__pycache__/__init__.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## text_processor/connection/__pycache__/kafka_connection_consumer.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## text_processor/connection/__pycache__/kafka_connection_producer.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## text_processor/connection/__pycache__/mongo_connection.cpython-314.pyc

**SKIPPED (binary or non-UTF8 text)**

## text_processor/connection/kafka_connection_consumer.py

```python
from confluent_kafka import Consumer
from dotenv import dotenv_values


ENV = dotenv_values(".env.local")

KAFKA_BOOTSTRAP_SERVERS = ENV.get("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")
KAFKA_GROUP_ID_TEXT = ENV.get("KAFKA_GROUP_ID_TEXT", "pizza-text")


class KafkaConsumerClient:
    def __init__(self, bootstrap_servers: str, group_id: str):
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })

    def subscribe(self, topic: str):
        self.consumer.subscribe([topic])

    def poll(self, timeout: float = 1.0):
        return self.consumer.poll(timeout)

    def close(self):
        self.consumer.close()

consumer = KafkaConsumerClient(KAFKA_BOOTSTRAP_SERVERS,KAFKA_GROUP_ID_TEXT)

```

## text_processor/connection/kafka_connection_producer.py

```python
from confluent_kafka import Producer
import json
from typing import Callable
from dotenv import dotenv_values


ENV = dotenv_values(".env.local")

KAFKA_BOOTSTRAP_SERVERS = ENV.get("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")


class KafkaProducerClient:
    def __init__(self, bootstrap_servers: str):
        self.producer = Producer({"bootstrap.servers": bootstrap_servers})

    def send(self, topic: str, value: bytes):
        self.producer.produce(topic=topic, value=value)

    def flush(self):
        self.producer.flush()

producer = KafkaProducerClient(KAFKA_BOOTSTRAP_SERVERS)
```

## text_processor/connection/mongo_connection.py

```python
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

# --- Config ---
ENV = dotenv_values(".env.local")
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

## text_processor/text_worker.py

```python
from .connection.kafka_connection_consumer import consumer
from .connection.mongo_connection import mongo
from .clean_preprocessor import clean_instructions
import json
import re

from dotenv import dotenv_values
ENV = dotenv_values(".env.local")

TOPIC_ORDERS = ENV.get("TOPIC_ORDERS", "pizza_orders")

collection = mongo.collection("pizza_orders")
consumer.subscribe(TOPIC_ORDERS)

# =============================
#   +-----------------------+
#   |     processes         |  
#   +-----------------------+

def allergy_label(order):
    """
    filter and label based on the code "allergy"
    """
    text = order["special_instructions"].lower()
    codes = ["allergy", "peanut", "gluten"]
    allergies_flagged = any(code in text for code in codes)

    upper_text = text.upper()
    cleaned_text = re.sub(r"[@#?$!().,]", "", upper_text)

    collection.update_one(
            {"order_id": order["order_id"]},
            {"$set": {"allergies_flaged": allergies_flagged,
                        "protocol_cleaned": cleaned_text}}
            )
    return cleaned_text



#   +-----------------------+
#   |     main              |  
#   +-----------------------+

def text_process():
    try:
        while True:
            order = consumer.poll(1.0) 
            if order is None: continue # validating you get an order and that it is not error
            if order.error():
                print(f"text error: {order.error()}")
                continue

            order = json.loads(order.value())
            clean_text = allergy_label(order)
            clean_instructions(order, clean_text)

    finally:
        consumer.close()

text_process()





# python -m text_processor.text_worker
```

