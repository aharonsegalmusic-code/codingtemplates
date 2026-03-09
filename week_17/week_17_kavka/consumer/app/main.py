import json
import os
import time

from sql_init import ensure_schema
from mysql_connection import db
from kafka_consumer import consumer
from confluent_kafka import KafkaError

kafka_topic = os.getenv("KAFKA_TOPIC", "raw-records")


def wait_for_mysql(max_seconds: int = 90, sleep_seconds: float = 2.0):
    deadline = time.time() + max_seconds
    last_err = None
    while time.time() < deadline:
        try:
            db.query("SELECT 1;")
            return
        except Exception as e:
            last_err = e
            print(f"MySQL not ready yet, retrying in {sleep_seconds}s... ({e})")
            time.sleep(sleep_seconds)
    raise RuntimeError(f"MySQL not ready after {max_seconds}s. Last error: {last_err}")


def upsert_customer(record: dict):
    sql = """
INSERT INTO customers (
  customerNumber, customerName, contactLastName, contactFirstName, phone,
  addressLine1, addressLine2, city, state, postalCode, country,
  salesRepEmployeeNumber, creditLimit
)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON DUPLICATE KEY UPDATE
  customerName=VALUES(customerName),
  contactLastName=VALUES(contactLastName),
  contactFirstName=VALUES(contactFirstName),
  phone=VALUES(phone),
  addressLine1=VALUES(addressLine1),
  addressLine2=VALUES(addressLine2),
  city=VALUES(city),
  state=VALUES(state),
  postalCode=VALUES(postalCode),
  country=VALUES(country),
  salesRepEmployeeNumber=VALUES(salesRepEmployeeNumber),
  creditLimit=VALUES(creditLimit);
""".strip()
    params = (
        record.get("customerNumber"),
        record.get("customerName"),
        record.get("contactLastName"),
        record.get("contactFirstName"),
        record.get("phone"),
        record.get("addressLine1"),
        record.get("addressLine2"),
        record.get("city"),
        record.get("state"),
        record.get("postalCode"),
        record.get("country"),
        record.get("salesRepEmployeeNumber"),
        record.get("creditLimit"),
    )
    db.execute(sql, params)


def upsert_order(record: dict):
    sql = """
INSERT INTO orders (
  orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber
)
VALUES (%s,%s,%s,%s,%s,%s,%s)
ON DUPLICATE KEY UPDATE
  orderDate=VALUES(orderDate),
  requiredDate=VALUES(requiredDate),
  shippedDate=VALUES(shippedDate),
  status=VALUES(status),
  comments=VALUES(comments),
  customerNumber=VALUES(customerNumber);
""".strip()
    params = (
        record.get("orderNumber"),
        record.get("orderDate"),
        record.get("requiredDate"),
        record.get("shippedDate"),
        record.get("status"),
        record.get("comments"),
        record.get("customerNumber"),
    )
    db.execute(sql, params)


def consume_loop(poll_seconds: int = 5):
    consumer.subscribe([kafka_topic])
    print(f"Consumer subscribed to topic={kafka_topic}")

    while True:
        msg = consumer.poll(poll_seconds)
        if msg is None:
            continue

        # FIX: handle kafka error events
        if msg.error():
            # Long-term fix: topic might not exist yet; wait and retry quietly
            if msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                time.sleep(2)
                continue
            print("Kafka message error:", msg.error())
            continue

        val = msg.value()
        # FIX: handle tombstone / empty messages
        if val is None or len(val) == 0:
            continue

        try:
            payload = val.decode("utf-8", errors="strict")
            record = json.loads(payload)
        except Exception as e:
            print("Skipping bad message:", e)
            continue

        record_type = record.get("type")
        if record_type == "customer":
            upsert_customer(record)
        elif record_type == "order":
            upsert_order(record)
        else:
            print("Unknown record type:", record_type)


if __name__ == "__main__":
    wait_for_mysql()
    ensure_schema()
    consume_loop()