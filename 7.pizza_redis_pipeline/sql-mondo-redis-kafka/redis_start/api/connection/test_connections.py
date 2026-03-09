from mysql_connection import get_mysql_connection
from redis_connection import r
from mongo_connection import mongo
from kafka_connection_producer import producer


def test_mysql():
    try:
        conn = get_mysql_connection()
        conn.close()
        print("MySQL: OK")
    except Exception as e:
        print(f"MySQL: FAIL - {e}")


def test_redis():
    try:
        r.ping()
        print("Redis: OK")
    except Exception as e:
        print(f"Redis: FAIL - {e}")


def test_mongo():
    try:
        mongo.client.admin.command("ping")
        print("Mongo: OK")
    except Exception as e:
        print(f"Mongo: FAIL - {e}")


def test_kafka():
    try:
        producer.producer.list_topics(timeout=5)
        print("Kafka: OK")
    except Exception as e:
        print(f"Kafka: FAIL - {e}")


if __name__ == "__main__":
    test_mysql()
    test_redis()
    test_mongo()
    test_kafka()
