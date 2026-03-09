# sql_test.py
#
# Goal
# - connect to MySQL using a small Database class
# - TEST DB NAME: ensure the database exists
# - TEST DB TABLES: ensure example tables exist (test_customers, test_orders)
# - run a few test queries and print results
#
# Reads configuration ONLY from an env file (NOT from OS environment)
#
# install:
#   pip install mysql-connector-python python-dotenv
#
# env files:
#   .env.local  (for running this script on your PC)
#   .env.prod   (for production)
#
# usage:
#   python sql_test.py

import mysql.connector
from mysql.connector import Error
from dotenv import dotenv_values

# =========================================================
# ENV FILE MODE (change this)
# =========================================================
PRODUCTION = False  # False -> .env.local, True -> .env.prod

ENV_PATH = ".env.prod" if PRODUCTION else ".env.local"
ENV = dotenv_values(ENV_PATH)  # NOTE: reads ONLY from the file, does NOT use os.environ


def must_get(key: str) -> str:
    v = ENV.get(key)
    if v is None or str(v).strip() == "":
        raise RuntimeError(f"Missing required key in {ENV_PATH}: {key}")
    return str(v)


# required env vars
MYSQL_HOST = must_get("MYSQL_HOST")
MYSQL_PORT = int(must_get("MYSQL_PORT"))
MYSQL_USER = must_get("MYSQL_USER")
MYSQL_PASSWORD = must_get("MYSQL_PASSWORD")
MYSQL_DB = must_get("MYSQL_DB")

# script flags (keep simple)
INIT_DB = True
INIT_SCHEMA = True


# =========================================================
# TEST SCHEMA (examples of common SQL types + relationship)
# =========================================================

CREATE_TEST_CUSTOMERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS test_customers (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

  full_name VARCHAR(150) NOT NULL,
  email VARCHAR(255) NULL,

  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  signup_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  age TINYINT UNSIGNED NULL,
  credit_limit DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  rating FLOAT NULL,
  balance DOUBLE NULL,

  birth_date DATE NULL,
  preferred_time TIME NULL,
  last_login DATETIME NULL,

  profile_text TEXT NULL,
  avatar_blob BLOB NULL,

  meta JSON NULL,
  uuid_bin BINARY(16) NULL,

  country_code CHAR(2) NULL,
  status ENUM('new','active','blocked') NOT NULL DEFAULT 'new',

  PRIMARY KEY (id),
  UNIQUE KEY uq_test_customers_email (email)
);
""".strip()

CREATE_TEST_ORDERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS test_orders (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  customer_id BIGINT UNSIGNED NOT NULL,

  order_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  total_amount DECIMAL(12,2) NOT NULL,
  status ENUM('pending','paid','shipped','cancelled') NOT NULL DEFAULT 'pending',

  note VARCHAR(255) NULL,
  extra JSON NULL,

  PRIMARY KEY (id),
  KEY idx_test_orders_customer_id (customer_id),

  CONSTRAINT fk_test_orders_customer
    FOREIGN KEY (customer_id) REFERENCES test_customers(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);
""".strip()


# =========================================================
# Database class
# =========================================================

class Database:
    def __init__(self, host: str, port: int, user: str, password: str):
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password

    def connect(self, database: str | None = None):
        kw = {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
        }
        if database:
            kw["database"] = database
        return mysql.connector.connect(**kw)

    def execute(self, sql: str, params=None, database: str | None = None) -> None:
        if params is None:
            params = ()

        conn = None
        cur = None
        try:
            conn = self.connect(database=database)
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
        finally:
            if cur is not None:
                try:
                    cur.close()
                except Exception:
                    pass
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass

    def query(self, sql: str, params=None, database: str | None = None):
        if params is None:
            params = ()

        conn = None
        cur = None
        try:
            conn = self.connect(database=database)
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur.fetchall()
        finally:
            if cur is not None:
                try:
                    cur.close()
                except Exception:
                    pass
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass


# =========================================================
# Tests
# =========================================================

def ensure_database(db: Database, db_name: str) -> None:
    rows = db.query("SHOW DATABASES;")
    names = {r[0] for r in rows}

    if db_name in names:
        print(f"TEST DB NAME: exists -> {db_name}")
        return

    print(f"TEST DB NAME: creating -> {db_name}")
    db.execute(f"CREATE DATABASE `{db_name}`;")
    print(f"TEST DB NAME: created -> {db_name}")


def ensure_schema(db: Database, db_name: str) -> None:
    print("TEST DB TABLES: ensuring tables (test_customers, test_orders)...")
    db.execute(CREATE_TEST_CUSTOMERS_TABLE_SQL, database=db_name)
    db.execute(CREATE_TEST_ORDERS_TABLE_SQL, database=db_name)
    print("TEST DB TABLES: ensured")


def main():
    print("mysql settings:")
    print(f"  host={MYSQL_HOST}")
    print(f"  port={MYSQL_PORT}")
    print(f"  user={MYSQL_USER}")
    print(f"  db={MYSQL_DB}")

    db = Database(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD)

    try:
        if INIT_DB:
            ensure_database(db, MYSQL_DB)

        if INIT_SCHEMA:
            ensure_schema(db, MYSQL_DB)

        tables = db.query("SHOW TABLES;", database=MYSQL_DB)
        table_names = [t[0] for t in tables]
        print("TEST DB TABLES: tables ->", table_names)

        c1 = db.query("SELECT COUNT(*) FROM test_customers;", database=MYSQL_DB)
        print("TEST DB TABLES: test_customers count ->", int(c1[0][0]))

        c2 = db.query("SELECT COUNT(*) FROM test_orders;", database=MYSQL_DB)
        print("TEST DB TABLES: test_orders count ->", int(c2[0][0]))

        print("OK sql_test completed")

    except Error as e:
        print("FAIL mysql:", e)
        raise


if __name__ == "__main__":
    main()