import os, json, asyncio
from fastapi import FastAPI, status
from confluent_kafka import Producer

from app.models import UserRegisterModel

app = FastAPI()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "users.registered")
SEED_FILE_PATH = os.getenv("SEED_FILE_PATH", "data/users_with_posts.json")


producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
                     'client.id': "fastAPI producer"})


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegisterModel):
    user_data = user.model_dump(mode="json")
 

    payload = json.dumps(user_data, ensure_ascii=False).encode("utf-8")
    producer.produce(KAFKA_TOPIC, payload)

    # TODO : 2 LINES!
    producer.flush(2)  # simplest: ensure it was sent before responding

    return {
        "status": "ok",
        "validated_user_id": user.user_id,
        "posts_count": len(user.posts),
        "topic": KAFKA_TOPIC,
    }


_seed_running = False  # simple flag (matches "while/flag" requirement)
async def seed_worker():
    global _seed_running
    _seed_running = True
    try:
        # 1) read file ONCE
        with open(SEED_FILE_PATH, "r", encoding="utf-8") as f:
            users = json.load(f)  # must be a LIST of users
        batch_size = 10
        # clear stop condition: i reaches end of list
        for i in range(0, len(users), batch_size):
            batch = users[i:i + batch_size]
            # validate + send each user
            for item in batch:
                user = UserRegisterModel.model_validate(item)
                payload = json.dumps(user.model_dump(mode="json"), ensure_ascii=False).encode("utf-8")
                producer.produce(KAFKA_TOPIC, value=payload)
            producer.flush(5)
            # 3) every 5 seconds send next batch (only if more batches exist)
            if i + batch_size < len(users):
                await asyncio.sleep(5)
    finally:
        _seed_running = False
        
@app.get("/seed")
async def seed():
    global _seed_running
    if not _seed_running:
        asyncio.create_task(seed_worker())
    return {
        "status": "started",
        "message": "seeding from file in batches of 10 every 5 seconds",
    }


