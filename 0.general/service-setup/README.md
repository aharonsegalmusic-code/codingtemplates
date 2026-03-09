# Dev Stack (Mongo + MySQL + Redis + Kafka) — Simple How-To

## 0) What this is
This project runs the “deps” (databases + Kafka + web UIs) in Docker, and you run the Python test scripts to verify everything works.

```bash
pip install confluent-kafka pymongo mysql-connector-python redis requests python-dotenv PyYAML
```


## 1) Start the deps (Docker)
From the project folder:

```bash
docker compose -f docker-compose.deps.yml up -d
```

### Stop deps
```bash
docker compose -f docker-compose.deps.yml down
```

### Stop deps + delete all data (full reset)
```bash
docker compose -f docker-compose.deps.yml down -v
```

---

## 2) Generate env files (local + docker)
Run:

```bash
python compose_to_env.py
```

This creates:
- `.env.local`  → use when Python runs on your computer (localhost)
- `.env.docker` → use when Python runs inside Docker (service names like `mysql`, `mongo`, `redis`, `kafka`)

✅ For this project (running tests on your PC), you will use **`.env.local`**.

---

## 3) Open the web UIs (optional but useful)
Use these URLs (your ports may differ if you changed them):

- Kafka UI: `http://127.0.0.1:18080`
- Mongo Express: `http://127.0.0.1:18081`
- CloudBeaver: `http://127.0.0.1:8978`
- RedisInsight: `http://127.0.0.1:5540`

---

## 4) Run the Python tests (in this order)
### 4.1 MySQL test (creates DB + tables and runs queries)
```bash
python sql_test.py
```
What you should see:
- `TEST DB NAME: exists -> suspicious`
- `TEST DB TABLES: ensured`
- counts for `test_customers` and `test_orders`

---

### 4.2 Mongo test (creates a collection + init doc so DB appears in UIs)
```bash
python mongo_test.py
```
What you should see:
- `TEST CONNECT: ping -> OK`
- collection exists
- a sample doc output

---

### 4.3 Kafka test (produce + consume the same message)
```bash
python kafka_test.py
```
What you should see:
- producer delivered message
- consumer received the same `run_id`

To view it in Kafka UI:
- open Kafka UI → Topics → `raw-records` → Messages → read from **Earliest**

---

### 4.4 Redis test (write keys + read them back)
```bash
python redis_test.py
```
What you should see:
- `ping -> True`
- it prints 3 created keys with prefix: `test:redis`

To view in RedisInsight:
- open RedisInsight → Browser → search for `test:redis`

---

## 5) Desktop apps (optional)
Use these only if you want desktop tools:

### Mongo Compass
Use:
```text
mongodb://app:app_pw@localhost:27017/?authSource=admin
```

### DBeaver Desktop (MySQL)
- Host: `localhost`
- Port: `3306`
- User: `root` (or `appuser` if you created it)
- Password: `root_pwd` (or `app_pwd`)
- Database: `suspicious`

---

## Files you use (in order)
1) `docker-compose.deps.yml`  → starts/stops the deps stack  
2) `compose_to_env.py`        → generates `.env.local` and `.env.docker`  
3) `.env.local`              → used by all Python test scripts (host-run)  
4) `sql_test.py`              → tests MySQL + creates test tables  
5) `mongo_test.py`            → tests Mongo + creates test collection/doc  
6) `kafka_test.py`            → tests Kafka (produce + consume)  
7) `redis_test.py`            → tests Redis (write + read + view in UI)  

---

## Quick summary
1) `docker compose ... up -d`  
2) `python compose_to_env.py`  
3) Run tests: `sql_test.py` → `mongo_test.py` → `kafka_test.py` → `redis_test.py`  
4) Open UIs to visually confirm data/messages/keys
```