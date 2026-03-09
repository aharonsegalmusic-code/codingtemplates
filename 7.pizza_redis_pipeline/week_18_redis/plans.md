  {
    "border": "jordan",
    "zone": "zone-10",
    "timestamp": "2026-02-15T23:32:58.011404",
    "people_count": 2,
    "weapons_count": 0,
    "vehicle_type": "none",
    "distance_from_fence_m": 722,
    "visibility_quality": 0.67
  }

  rout 3 range 
  dict = {"close": 0 <x>301,
        "medium": 301-800,
        "far": 801-1500}


COMPONENT PRODUDER

"""
Producer - alert insert and priority classification

INPUT:
    - json: list -> border camera alerts

OUTPUT:
    - alerts pushed to redis queues (queue_urgent / queue_normal)

FLOW:
    json file -> producer -> redis queues
"""
    connects only to redis

    load data
        set PRIORITY
        enter into que based on priority
            Urgent/Normal
    INCLUDES -> CONSUMER
        pulls alerts based on PRIORITY
        saves then in the db 
        add INSERTION_TIME  

COMPONENT REDIS
    HANDLES priority order


in mongo group by 