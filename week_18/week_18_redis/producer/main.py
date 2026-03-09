"""
Producer - alert ingestion and priority classification

INPUT:
    - json file containing array of border camera alerts

OUTPUT:
    - alerts pushed to redis queues (queue_urgent / queue_normal)

FLOW:
    json file -> producer -> redis queues

NOTE: in the compose
        restart: "no"
        so that the code runs once
"""

import json
from dotenv import dotenv_values
from redis_connection import r
from priority_logic import classify

config = dotenv_values(".env")

ALERTS_FILE = r"border_alerts.json"

QUEUE_URGENT = "urgent_queue"
QUEUE_NORMAL = "normal_queue"


def load_alerts(file_path):
    # read json file 
    with open(file_path, "r") as f: 
        return json.load(f)
    

def process_alerts():
    print("producer starting...")
    alerts = load_alerts(ALERTS_FILE)
    print(f"loaded {len(alerts)} alerts")

    urgent_count = 0
    normal_count = 0

    for alert in alerts:
        # classify and add priority field
        priority = classify(alert)
        alert["priority"] = priority

        # we have 2 lists in redis
        # 1 :QUEUE_URGENT
        # 2 :QUEUE_NORMAL
        alert_r = json.dumps(alert)

        if priority == "URGENT":
            # rpush(list_name, *values) to the end
            r.rpush(QUEUE_URGENT, alert_r)
            urgent_count += 1
        else:
            r.rpush(QUEUE_NORMAL, alert_r)
            normal_count += 1

    print(f"done - urgent: {urgent_count}, normal: {normal_count}")


process_alerts()