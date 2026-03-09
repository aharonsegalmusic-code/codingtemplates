# kafka_producer_consumer_template.py
#
# What you get
# - A PRODUCER SECTION you can copy anywhere (create_producer + send_event)
# - A CONSUMER SECTION you can copy anywhere (create_consumer + poll loop)
# - A demo main() that sends one message and then consumes it back so you can see the flow
#
# Install:
#   pip install confluent-kafka python-dotenv
#
# Env (example for host-run):
#   KAFKA_BOOTSTRAP_SERVERS=127.0.0.1:9092
#   KAFKA_TOPIC=raw-records

from __future__ import annotations

import json
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from dotenv import dotenv_values

# ---------- ENV FILE (read only from file, not OS env) ----------
ENV = dotenv_values(".env.local")  # change to .env.prod if you want


def must_get(key: str) -> str:
    v = ENV.get(key)
    if v is None or str(v).strip() == "":
        raise RuntimeError(f"Missing required key in .env.local: {key}")
    return str(v)


KAFKA_BOOTSTRAP_SERVERS = must_get("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = must_get("KAFKA_TOPIC")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# =========================================================
# PRODUCER SECTION (copy this)
# =========================================================

def create_producer(bootstrap_servers: str):
    """
    Create a Kafka producer.
    Copy this function into your project and call it once at startup.
    """
    from confluent_kafka import Producer

    conf = {
        "bootstrap.servers": bootstrap_servers,
        "acks": "all",
        "message.timeout.ms": 10000,
        # good defaults for dev
        "enable.idempotence": True,
        "retries": 3,
    }
    return Producer(conf)


def send_event(producer, topic: str, key: str, value: Dict[str, Any]) -> None:
    """
    Send ONE json message to Kafka.
    Copy this into your project.
    """
    payload = json.dumps(value, ensure_ascii=False).encode("utf-8")

    def on_delivery(err, msg):
        if err is not None:
            raise RuntimeError(f"delivery failed: {err}")
        print(f"PRODUCER: delivered topic={msg.topic()} partition={msg.partition()} offset={msg.offset()} key={key}")

    producer.produce(topic=topic, key=key.encode("utf-8"), value=payload, on_delivery=on_delivery)
    producer.flush(10)


# =========================================================
# CONSUMER SECTION (copy this)
# =========================================================

def create_consumer(bootstrap_servers: str, group_id: str):
    """
    Create a Kafka consumer.
    Copy this function into your project and call it once at startup.
    """
    from confluent_kafka import Consumer

    conf = {
        "bootstrap.servers": bootstrap_servers,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
        # dev-friendly timeouts
        "session.timeout.ms": 10000,
    }
    return Consumer(conf)


def poll_one(consumer, timeout_seconds: float = 1.0) -> Optional[Dict[str, Any]]:
    """
    Poll ONE message, return parsed json dict or None.
    Copy this into your project.
    """
    msg = consumer.poll(timeout_seconds)
    if msg is None:
        return None
    if msg.error():
        # ignore partition EOF, raise other errors
        err_s = str(msg.error())
        if "PARTITION_EOF" in err_s:
            return None
        raise RuntimeError(f"consumer error: {msg.error()}")

    key = msg.key().decode("utf-8", errors="replace") if msg.key() else ""
    raw = msg.value().decode("utf-8", errors="replace")
    try:
        value = json.loads(raw)
    except Exception:
        value = {"_raw": raw}

    event = {
        "key": key,
        "topic": msg.topic(),
        "partition": msg.partition(),
        "offset": msg.offset(),
        "value": value,
    }
    return event


# =========================================================
# DEMO (send one message, then read until we see it)
# =========================================================

def main():
    run_id = uuid.uuid4().hex
    key = run_id

    # --- Producer demo ---
    producer = create_producer(KAFKA_BOOTSTRAP_SERVERS)

    data = {
        "type": "kafka_flow_demo",
        "run_id": run_id,
        "ts": now_iso(),
        "msg": "hello from producer",
        "n": 1,
    }

    print("=== FLOW STEP 1: PRODUCE ===")
    print(f"bootstrap={KAFKA_BOOTSTRAP_SERVERS}")
    print(f"topic={KAFKA_TOPIC}")
    print(f"run_id={run_id}")
    send_event(producer, KAFKA_TOPIC, key, data)

    # --- Consumer demo ---
    print("\n=== FLOW STEP 2: CONSUME ===")
    group_id = f"flow-demo-{run_id}"
    consumer = create_consumer(KAFKA_BOOTSTRAP_SERVERS, group_id)
    consumer.subscribe([KAFKA_TOPIC])

    deadline = time.time() + 12
    try:
        while time.time() < deadline:
            event = poll_one(consumer, timeout_seconds=1.0)
            if not event:
                continue

            print(f"CONSUMER: got key={event['key']} offset={event['offset']} value={event['value']}")
            if event["key"] == run_id and isinstance(event["value"], dict) and event["value"].get("run_id") == run_id:
                print("OK FLOW: consumer received the same run_id produced")
                break
        else:
            raise SystemExit("FAIL FLOW: did not see the produced message within timeout")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()