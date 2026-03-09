import os
import time
from datetime import datetime

from pymongo import MongoClient
from bson import ObjectId

import mysql.connector


# -----------------------------
# ENV (minimal, defaults match your project)
# -----------------------------
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://app:app_pw@127.0.0.1:27017/social_commerce?authSource=admin",
)
MONGO_DB = os.getenv("MONGO_DB", "social_commerce")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "mini_users")  # <- your Beanie collection name

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3307"))
MYSQL_DB = os.getenv("MYSQL_DB", "social_commerce")
MYSQL_USER = os.getenv("MYSQL_USER", "app")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "app_pw")

ETL_BATCH_SIZE = int(os.getenv("ETL_BATCH_SIZE", "50"))
ETL_POLL_SECONDS = int(os.getenv("ETL_POLL_SECONDS", "5"))

STATE_KEY = os.getenv("ETL_STATE_KEY", "mongo_to_mysql_users")  # identifies this ETL job


# -----------------------------
# MySQL: schema + state table
# -----------------------------
DDL_USERS = """
CREATE TABLE IF NOT EXISTS users_etl (
  user_id VARCHAR(64) PRIMARY KEY,
  full_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  age INT NOT NULL,
  phone VARCHAR(32) NULL,
  city VARCHAR(255) NULL,
  created_at DATETIME NULL,
  insertion_time DATETIME NOT NULL
);
"""

DDL_POSTS = """
CREATE TABLE IF NOT EXISTS posts_etl (
  post_id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  title VARCHAR(255) NOT NULL,
  published_at DATETIME NULL,
  content TEXT NOT NULL
);
"""

DDL_STATE = """
CREATE TABLE IF NOT EXISTS etl_state (
  id VARCHAR(64) PRIMARY KEY,
  last_insertion_time DATETIME NULL,
  last_mongo_id VARCHAR(32) NULL
);
"""


def mysql_connect():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        autocommit=False,
    )


def init_mysql_schema(conn):
    cur = conn.cursor()
    cur.execute(DDL_USERS)
    cur.execute(DDL_POSTS)
    cur.execute(DDL_STATE)
    conn.commit()
    cur.close()


def get_state(conn):
    cur = conn.cursor()
    cur.execute("SELECT last_insertion_time, last_mongo_id FROM etl_state WHERE id=%s", (STATE_KEY,))
    row = cur.fetchone()
    if row is None:
        cur.execute(
            "INSERT INTO etl_state (id, last_insertion_time, last_mongo_id) VALUES (%s, %s, %s)",
            (STATE_KEY, None, None),
        )
        conn.commit()
        cur.close()
        return None, None

    cur.close()
    return row[0], row[1]


def set_state(conn, last_insertion_time, last_mongo_id):
    cur = conn.cursor()
    cur.execute(
        "UPDATE etl_state SET last_insertion_time=%s, last_mongo_id=%s WHERE id=%s",
        (last_insertion_time, last_mongo_id, STATE_KEY),
    )
    conn.commit()
    cur.close()


# -----------------------------
# Transform: flatten Mongo JSON -> MySQL rows
# -----------------------------
def to_users_row(doc):
    # Expect doc has insertion_time (you added it in Beanie)
    return (
        str(doc.get("user_id", "")),
        doc.get("full_name", ""),
        doc.get("email", ""),
        int(doc.get("age", 0)),
        doc.get("phone"),
        doc.get("city"),
        doc.get("created_at"),       # datetime or None
        doc.get("insertion_time"),   # datetime (required for ETL)
    )


def to_posts_rows(doc):
    user_id = str(doc.get("user_id", ""))
    posts = doc.get("posts") or []
    rows = []
    for p in posts:
        rows.append(
            (
                p.get("post_id", ""),
                user_id,
                p.get("title", ""),
                p.get("published_at"),
                p.get("content", ""),
            )
        )
    return rows


# -----------------------------
# Load: insert/upsert into MySQL
# -----------------------------
SQL_UPSERT_USER = """
INSERT INTO users_etl (user_id, full_name, email, age, phone, city, created_at, insertion_time)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
ON DUPLICATE KEY UPDATE
  full_name=VALUES(full_name),
  email=VALUES(email),
  age=VALUES(age),
  phone=VALUES(phone),
  city=VALUES(city),
  created_at=VALUES(created_at),
  insertion_time=VALUES(insertion_time);
"""

SQL_UPSERT_POST = """
INSERT INTO posts_etl (post_id, user_id, title, published_at, content)
VALUES (%s,%s,%s,%s,%s)
ON DUPLICATE KEY UPDATE
  user_id=VALUES(user_id),
  title=VALUES(title),
  published_at=VALUES(published_at),
  content=VALUES(content);
"""


def load_batch(conn, docs):
    cur = conn.cursor()

    user_rows = [to_users_row(d) for d in docs]
    cur.executemany(SQL_UPSERT_USER, user_rows)

    post_rows = []
    for d in docs:
        post_rows.extend(to_posts_rows(d))
    if post_rows:
        cur.executemany(SQL_UPSERT_POST, post_rows)

    conn.commit()
    cur.close()


# -----------------------------
# Mongo read: incremental by insertion_time (+ tie-breaker by _id)
# -----------------------------
def build_query(last_time, last_id):
    base = {"insertion_time": {"$exists": True}}

    if last_time is None:
        # first run: take oldest first
        return base

    if last_id is None:
        return {"$and": [base, {"insertion_time": {"$gt": last_time}}]}

    # handle ties: same insertion_time but _id greater than last processed
    return {
        "$and": [
            base,
            {
                "$or": [
                    {"insertion_time": {"$gt": last_time}},
                    {"insertion_time": last_time, "_id": {"$gt": ObjectId(last_id)}},
                ]
            },
        ]
    }


def main():
    # Mongo
    mongo = MongoClient(MONGO_URI)
    col = mongo[MONGO_DB][MONGO_COLLECTION]

    # MySQL
    mysql_conn = mysql_connect()
    init_mysql_schema(mysql_conn)

    last_time, last_id = get_state(mysql_conn)

    print("ETL started")
    print(f"- Mongo: {MONGO_DB}.{MONGO_COLLECTION}")
    print(f"- MySQL: {MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}")
    print(f"- Batch size: {ETL_BATCH_SIZE}, Poll seconds: {ETL_POLL_SECONDS}")
    print(f"- State key: {STATE_KEY}, last_time={last_time}, last_id={last_id}")

    while True:
        q = build_query(last_time, last_id)

        cursor = (
            col.find(q)
            .sort([("insertion_time", 1), ("_id", 1)])
            .limit(ETL_BATCH_SIZE)
        )
        docs = list(cursor)

        if not docs:
            time.sleep(ETL_POLL_SECONDS)
            continue

        # Load to MySQL (flatten + upsert)
        load_batch(mysql_conn, docs)

        # Update state checkpoint to last doc in this batch
        last_doc = docs[-1]
        last_time = last_doc.get("insertion_time")
        last_id = str(last_doc.get("_id"))

        set_state(mysql_conn, last_time, last_id)

        print(
            f"Loaded {len(docs)} users. "
            f"New checkpoint: insertion_time={last_time}, _id={last_id}"
        )


if __name__ == "__main__":
    main()