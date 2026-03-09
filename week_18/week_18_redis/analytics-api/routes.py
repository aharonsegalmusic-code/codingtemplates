"""
return the analytics based on query
    first check if there are results stored for this query in redis
    if not it makes it from mongo and stores in redis

    all routs have the exact same build 
        no input
        try to read from redis
        else make from mongo
        save to redis
    CACHE_TTL -> the number of seconds until {cache_key} will expire
"""

import json
from fastapi import APIRouter
from redis_connection import r
from dotenv import dotenv_values
from dal import (
    get_alerts_by_border_and_priority,
    get_top_urgent_zones,
    get_distance_distribution,
    get_low_visibility_high_activity,
    get_hot_zones,
)

config = dotenv_values(".env")

CACHE_TTL = int(config.get("CACHE_TTL", "60"))

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@router.get("/alerts-by-border-and-priority")
def alerts_by_border_and_priority():
    # cache aside pattern for border and priority distribution
    cache_key = "analytics:alerts_by_border_and_priority"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    result = get_alerts_by_border_and_priority()
    r.set(cache_key, json.dumps(result), ex=CACHE_TTL)
    return result


@router.get("/top-urgent-zones")
def top_urgent_zones():
    # cache aside pattern for top 5 urgent zones
    cache_key = "analytics:top_urgent_zones"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    result = get_top_urgent_zones()
    r.set(cache_key, json.dumps(result), ex=CACHE_TTL)
    return result


@router.get("/distance-distribution")
def distance_distribution():
    # cache aside pattern for distance range distribution
    cache_key = "analytics:distance_distribution"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    result = get_distance_distribution()
    r.set(cache_key, json.dumps(result), ex=CACHE_TTL)
    return result


@router.get("/low-visibility-high-activity")
def low_visibility_high_activity():
    # cache aside pattern for low visibility high activity zones
    cache_key = "analytics:low_visibility_high_activity"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    result = get_low_visibility_high_activity()
    r.set(cache_key, json.dumps(result), ex=CACHE_TTL)
    return result


@router.get("/hot-zones")
def hot_zones():
    # cache aside pattern for hot zones
    cache_key = "analytics:hot_zones"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    result = get_hot_zones()
    r.set(cache_key, json.dumps(result), ex=CACHE_TTL)
    return result