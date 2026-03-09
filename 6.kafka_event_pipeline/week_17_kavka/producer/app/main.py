"""
THE PRODUCER APP
this gets data from mogodb 
and send it to kafka
    the sending is done in batches of 30 
    and during each batch sends each document individually in 0.5 second intervals
"""

import os
from fastapi import FastAPI

from .routes import router
from .kafka_publisher import ensure_topic_exists

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
def on_startup():
    topic = os.getenv("KAFKA_TOPIC", "raw-records")
    ensure_topic_exists(topic)