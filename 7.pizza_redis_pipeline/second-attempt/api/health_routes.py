from fastapi import APIRouter
from .connection.mongo_connection import mongo
from .connection.redis_connection import get_redis_client
from .connection.kafka_connection_producer import producer
from .connection.mysql_connection import get_mysql_connection

health_router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@health_router.get("/api")
def ping_api():
    return {"status": "ok", "service": "api"}

@health_router.get("/mongo")
def ping_mongo():
    try:
        collections = mongo.db.list_collection_names()
        if not collections:
            return {"status": "ok", "service": "mongo", "message": "connected but no collections yet"}
        return {"status": "ok", "service": "mongo", "collections": collections}
    except Exception as e:
        return {"status": "error", "service": "mongo", "message": str(e)}

@health_router.get("/redis")
def ping_redis():
    try:
        r = get_redis_client()
        r.ping()
        return {"status": "ok", "service": "redis"}
    except Exception as e:
        return {"status": "error", "service": "redis", "message": str(e)}


@health_router.get("/kafka")
def ping_kafka():
    try:
        producer
        return {"status": "ok", "service": "kafka"}
    except Exception as e:
        return {"status": "error", "service": "kafka", "message": str(e)}


@health_router.get("/mysql")
def ping_mysql():
    try:
        conn = get_mysql_connection()
        conn.ping(reconnect=True)
        conn.close()
        return {"status": "ok", "service": "mysql"}
    except Exception as e:
        return {"status": "error", "service": "mysql", "message": str(e)}
