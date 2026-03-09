"""
connection_test.py

Goal:
- One file you can run locally to test connectivity to: MongoDB, MySQL, Kafka, Redis + Web UIs
- Config dict controls what to test (default: test everything)
- Options to init Mongo collection + init MySQL schema (create DB/tables) + init Kafka topic

Install (pick what you use):
  pip install pymongo mysql-connector-python redis requests confluent-kafka

Run:
  python connection_test.py
  # optional output file:
  python connection_test.py --out connection_report.txt

Notes about "UI connected to DB":
- Kafka UI: we can check UI is up and try /actuator/health. True DB connectivity still depends on its config.
- Mongo Express: we can detect common "cannot connect" text in HTML.
- CloudBeaver / RedisInsight: UI can be up while NOT connected yet (connections are configured inside the UI).
"""

import argparse
import datetime
import json
import os
import sys
from typing import Any, Dict, List, Tuple

# =========================================================
# ENV VARS (edit here or set in your shell)
# =========================================================

# --- Mongo ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://app:app_pw@127.0.0.1:27017/?authSource=admin")
MONGO_DB = os.getenv("MONGO_DB", "suspicious")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "records")

# --- MySQL ---
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")          # or "appuser" if you created it
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root_pwd")
MYSQL_DB = os.getenv("MYSQL_DB", "suspicious")

# --- Kafka ---
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "raw-records")

# --- Redis ---
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")  # empty by default

# --- Web UIs (edit ports to match your compose) ---
KAFKA_UI_URL = os.getenv("KAFKA_UI_URL", "http://127.0.0.1:18080")
MONGO_EXPRESS_URL = os.getenv("MONGO_EXPRESS_URL", "http://127.0.0.1:18081")
CLOUDBEAVER_URL = os.getenv("CLOUDBEAVER_URL", "http://127.0.0.1:8978")
REDISINSIGHT_URL = os.getenv("REDISINSIGHT_URL", "http://127.0.0.1:5540")

# =========================================================
# CONFIG (flip to False if you don't want to test something)
# =========================================================

CONFIG: Dict[str, Any] = {
    # what to test
    "test_mongo": True,
    "test_mysql": True,
    "test_kafka": True,
    "test_redis": True,
    "test_web_uis": True,

    # init options
    "init_mongo_collection": False,   # create DB+collection by writing a tiny init doc
    "init_mysql_db": False,           # create DB if missing
    "init_mysql_schema": False,       # create customers/orders tables
    "init_kafka_topic": False,        # create topic if missing (single partition, rf=1)

    # ui checks (simple)
    "ui_timeout_seconds": 3.0,
}

# =========================================================
# Helpers
# =========================================================

def ts() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def banner(title: str) -> str:
    line = "=" * (len(title) + 8)
    return f"\n{line}\n=== {title} ===\n{line}"


def safe_import(name: str):
    try:
        return __import__(name)
    except Exception as e:
        return None


class Reporter:
    def __init__(self):
        self.lines: List[str] = []

    def write(self, s: str):
        print(s)
        self.lines.append(s)

    def dump_to_file(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines) + "\n")


# =========================================================
# Tests
# =========================================================

def test_web_uis(r: Reporter, timeout_seconds: float):
    requests = safe_import("requests")
    if requests is None:
        r.write("SKIP web uis: missing dependency 'requests' -> pip install requests")
        return

    def check(url: str, name: str, health_path: str = ""):
        try_urls = [url]
        if health_path:
            try_urls = [url.rstrip("/") + health_path, url]

        ok = False
        details = []
        for u in try_urls:
            try:
                resp = requests.get(u, timeout=timeout_seconds)
                details.append(f"{u} -> {resp.status_code}")
                if 200 <= resp.status_code < 500:
                    ok = True

                # extra heuristics
                body = ""
                try:
                    body = resp.text[:2000].lower()
                except Exception:
                    body = ""

                if "mongo-express" in name.lower():
                    if "could not connect" in body or "error" in body and "mongodb" in body:
                        details.append("NOTE mongo-express page contains error text (may not be connected to mongo)")
                if "kafka ui" in name.lower():
                    # actuator health sometimes returns json, show it if possible
                    if "actuator/health" in u and resp.headers.get("content-type", "").lower().startswith("application/json"):
                        try:
                            details.append("health: " + json.dumps(resp.json(), ensure_ascii=False))
                        except Exception:
                            pass

            except Exception as e:
                details.append(f"{u} -> ERROR {e}")

        status = "OK" if ok else "FAIL"
        r.write(f"{status} {name}: " + " | ".join(details))

    r.write(banner("WEB UI CHECKS"))
    check(KAFKA_UI_URL, "Kafka UI", health_path="/actuator/health")
    check(MONGO_EXPRESS_URL, "Mongo Express")
    check(CLOUDBEAVER_URL, "CloudBeaver")
    check(REDISINSIGHT_URL, "RedisInsight")
    r.write("NOTE: CloudBeaver/RedisInsight can be UP without being connected to DB yet (connections are configured inside the UI).")


def test_redis(r: Reporter):
    redis_mod = safe_import("redis")
    if redis_mod is None:
        r.write("SKIP redis: missing dependency 'redis' -> pip install redis")
        return

    r.write(banner("REDIS"))
    try:
        client = redis_mod.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD if REDIS_PASSWORD else None,
            socket_connect_timeout=3,
            socket_timeout=3,
            decode_responses=True,
        )
        pong = client.ping()
        r.write(f"OK redis ping: {pong}  (host={REDIS_HOST} port={REDIS_PORT})")

        # tiny optional smoke op
        client.set("_conn_test", "1", ex=30)
        val = client.get("_conn_test")
        r.write(f"OK redis set/get: _conn_test={val}")
    except Exception as e:
        r.write(f"FAIL redis: {e}")


def test_mongo(r: Reporter, init_collection: bool):
    pymongo = safe_import("pymongo")
    if pymongo is None:
        r.write("SKIP mongo: missing dependency 'pymongo' -> pip install pymongo")
        return

    r.write(banner("MONGODB"))
    try:
        from pymongo import MongoClient  # type: ignore
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)

        # ping
        client.admin.command("ping")
        r.write(f"OK mongo ping  (uri={MONGO_URI})")

        db_names = client.list_database_names()
        db_exists = MONGO_DB in db_names
        r.write(f"INFO mongo db exists? {db_exists}  (db={MONGO_DB})")

        db = client[MONGO_DB]

        if init_collection:
            col = db[MONGO_COLLECTION]
            init_doc = {"_init": True, "ts": ts()}
            res = col.insert_one(init_doc)
            col.delete_one({"_id": res.inserted_id})
            r.write(f"OK mongo init: ensured collection exists by insert/delete  (collection={MONGO_COLLECTION})")

        # after init, re-check
        col_names = db.list_collection_names()
        r.write(f"INFO mongo collections in '{MONGO_DB}': {col_names}")

    except Exception as e:
        r.write(f"FAIL mongo: {e}")


def mysql_schema_sql() -> List[str]:
    create_customers = """
CREATE TABLE IF NOT EXISTS customers (
  customerNumber INT NOT NULL,
  customerName VARCHAR(255) NULL,
  contactLastName VARCHAR(255) NULL,
  contactFirstName VARCHAR(255) NULL,
  phone VARCHAR(50) NULL,
  addressLine1 VARCHAR(255) NULL,
  addressLine2 VARCHAR(255) NULL,
  city VARCHAR(100) NULL,
  state VARCHAR(100) NULL,
  postalCode VARCHAR(20) NULL,
  country VARCHAR(100) NULL,
  salesRepEmployeeNumber INT NULL,
  creditLimit DECIMAL(12,2) NULL,
  PRIMARY KEY (customerNumber)
);
""".strip()

    create_orders = """
CREATE TABLE IF NOT EXISTS orders (
  orderNumber INT NOT NULL,
  orderDate DATE NULL,
  requiredDate DATE NULL,
  shippedDate DATE NULL,
  status VARCHAR(50) NULL,
  comments TEXT NULL,
  customerNumber INT NOT NULL,
  PRIMARY KEY (orderNumber),
  CONSTRAINT orders_customerNumber_fk FOREIGN KEY (customerNumber) REFERENCES customers(customerNumber)
);
""".strip()

    return [create_customers, create_orders]


def test_mysql(r: Reporter, init_db: bool, init_schema: bool):
    mysql_connector = safe_import("mysql.connector")
    if mysql_connector is None:
        r.write("SKIP mysql: missing dependency 'mysql-connector-python' -> pip install mysql-connector-python")
        return

    r.write(banner("MYSQL"))

    def connect(database: str = ""):
        import mysql.connector  # type: ignore
        kw = {
            "host": MYSQL_HOST,
            "port": MYSQL_PORT,
            "user": MYSQL_USER,
            "password": MYSQL_PASSWORD,
        }
        if database:
            kw["database"] = database
        return mysql.connector.connect(**kw)

    try:
        # connect to server (no db) to check/create db
        conn = connect("")
        cur = conn.cursor()

        cur.execute("SHOW DATABASES;")
        dbs = [row[0] for row in cur.fetchall()]
        exists = MYSQL_DB in dbs
        r.write(f"INFO mysql database exists? {exists}  (db={MYSQL_DB})")

        if (not exists) and init_db:
            cur.execute(f"CREATE DATABASE `{MYSQL_DB}`;")
            conn.commit()
            r.write(f"OK mysql init: created database '{MYSQL_DB}'")

        cur.close()
        conn.close()

        # connect to target db
        conn2 = connect(MYSQL_DB)
        cur2 = conn2.cursor()
        cur2.execute("SELECT DATABASE();")
        r.write(f"OK mysql connected to db: {cur2.fetchone()[0]}  (host={MYSQL_HOST} port={MYSQL_PORT} user={MYSQL_USER})")

        if init_schema:
            for stmt in mysql_schema_sql():
                cur2.execute(stmt)
            conn2.commit()
            r.write("OK mysql init: ensured tables customers + orders exist")

        # show tables
        cur2.execute("SHOW TABLES;")
        tables = [row[0] for row in cur2.fetchall()]
        r.write(f"INFO mysql tables in '{MYSQL_DB}': {tables}")

        cur2.close()
        conn2.close()

    except Exception as e:
        r.write(f"FAIL mysql: {e}")
        r.write("NOTE: If using CloudBeaver and you see 'Public Key Retrieval is not allowed', create a mysql_native_password user via init sql and use that user.")


def test_kafka(r: Reporter, init_topic: bool):
    ck = safe_import("confluent_kafka")
    if ck is None:
        r.write("SKIP kafka: missing dependency 'confluent-kafka' -> pip install confluent-kafka")
        return

    r.write(banner("KAFKA"))
    try:
        from confluent_kafka.admin import AdminClient, NewTopic  # type: ignore

        admin = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})

        md = admin.list_topics(timeout=5)
        r.write(f"OK kafka reachable: brokers={len(md.brokers)}  (bootstrap={KAFKA_BOOTSTRAP_SERVERS})")

        topics = set(md.topics.keys())
        has_topic = KAFKA_TOPIC in topics
        r.write(f"INFO kafka topic exists? {has_topic}  (topic={KAFKA_TOPIC})")

        if (not has_topic) and init_topic:
            fs = admin.create_topics([NewTopic(KAFKA_TOPIC, num_partitions=1, replication_factor=1)])
            f = fs[KAFKA_TOPIC]
            f.result(timeout=10)
            r.write(f"OK kafka init: created topic '{KAFKA_TOPIC}'")

        # re-list
        md2 = admin.list_topics(timeout=5)
        r.write(f"INFO kafka topics count: {len(md2.topics.keys())}")

    except Exception as e:
        r.write(f"FAIL kafka: {e}")
        r.write("NOTE: If this fails when running on host, bootstrap should be like 127.0.0.1:9092 (not kafka:29092).")


# =========================================================
# Main
# =========================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="", help="output report file path (txt)")
    args = parser.parse_args()

    default_out = "connection_report_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
    out_path = args.out.strip() or default_out

    r = Reporter()
    r.write("connection test report")
    r.write("generated at: " + ts())
    r.write("python: " + sys.version.replace("\n", " "))
    r.write("")

    r.write(banner("CONFIG"))
    r.write(json.dumps(CONFIG, indent=2))

    r.write(banner("ENV SUMMARY"))
    r.write("  cat > .env <<'ENV'")
    r.write(f"MONGO_URI={MONGO_URI}")
    r.write(f"MONGO_DB={MONGO_DB}")
    r.write(f"MONGO_COLLECTION={MONGO_COLLECTION}")
    r.write(f"MYSQL_HOST={MYSQL_HOST}")
    r.write(f"MYSQL_PORT={MYSQL_PORT}")
    r.write(f"MYSQL_USER={MYSQL_USER}")
    r.write(f"MYSQL_DB={MYSQL_DB}")
    r.write(f"KAFKA_BOOTSTRAP_SERVERS={KAFKA_BOOTSTRAP_SERVERS}")
    r.write(f"KAFKA_TOPIC={KAFKA_TOPIC}")
    r.write(f"REDIS_HOST={REDIS_HOST}")
    r.write(f"REDIS_PORT={REDIS_PORT}")
    r.write(f"KAFKA_UI_URL={KAFKA_UI_URL}")
    r.write(f"MONGO_EXPRESS_URL={MONGO_EXPRESS_URL}")
    r.write(f"CLOUDBEAVER_URL={CLOUDBEAVER_URL}")
    r.write(f"REDISINSIGHT_URL={REDISINSIGHT_URL}")
    r.write("ENV")


    if CONFIG.get("test_web_uis", True):
        test_web_uis(r, timeout_seconds=float(CONFIG.get("ui_timeout_seconds", 3.0)))

    if CONFIG.get("test_redis", True):
        test_redis(r)

    if CONFIG.get("test_mongo", True):
        test_mongo(r, init_collection=bool(CONFIG.get("init_mongo_collection", False)))

    if CONFIG.get("test_mysql", True):
        test_mysql(
            r,
            init_db=bool(CONFIG.get("init_mysql_db", False)),
            init_schema=bool(CONFIG.get("init_mysql_schema", False)),
        )

    if CONFIG.get("test_kafka", True):
        test_kafka(r, init_topic=bool(CONFIG.get("init_kafka_topic", False)))

    r.write(banner("DONE"))
    r.write(f"wrote report to: {os.path.abspath(out_path)}")
    r.dump_to_file(out_path)

 
if __name__ == "__main__":
    main()