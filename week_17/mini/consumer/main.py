
import os, json, asyncio
from confluent_kafka import Consumer, KafkaError
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, Document
from pydantic import EmailStr
from datetime import datetime 

from models import User

# TODO ADD INSERTION TIME 

async def consume():
    client = AsyncIOMotorClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
    await init_beanie(database=client[os.getenv("MONGO_DB", "social_commerce")], document_models=[User])

    consumer = Consumer({
        'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        'group.id': os.getenv("KAFKA_GROUP_ID", "user_group"),
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([os.getenv("KAFKA_TOPIC", "users.registered")])

    try:
        while True:
            print("-----test-----")
            msg = consumer.poll(0.1)
            if msg is None:
                await asyncio.sleep(0.01)
                continue
            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    print(msg.error())
                continue

            try:
                user = User(**json.loads(msg.value().decode('utf-8')))

                now = datetime.utcnow()


                await user.insert()
                print(f"Saved: {user.email}")
            except Exception as e:
                print(f"Error: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":    
    asyncio.run(consume())