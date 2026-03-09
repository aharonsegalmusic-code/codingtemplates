"""
    get_alerts_by_border_and_priority:
        - order boarders based on count of documents (disregarding priority)

    get_top_urgent_zones:
        - order boarders based on count or URGENT
        - top 5 

    get_distance_distribution:
        distances = "close": 0 - 300,
                    "medium": 301-800,
                    "far": 801- 1500,
                    use bucket [0, 300, 800]
        return count of each bucket

    get_low_visibility_high_activity:
        # find zones with high people count and low visibility 
            low visibility = (under 0.5)
            high people count = get avg for people count then check if bigger

    get_hot_zones:
        # find zones with high urgent count and low average distance from fence
            high urgent count = get avg for urgent count then check if bigger
"""


from mongo_connection import mongo

collection = mongo.collection("alerts")


def get_alerts_by_border_and_priority():
    # order boarders based on count of documents (disregarding priority)
    pipeline = [
        {
            "$group": {
                "_id": {"border": "$border"},
                "count": {"$sum": 1}
            }
        },
    ]
    results = list(collection.aggregate(pipeline))

    # reshape into readable format
    output = {}
    for item in results:
        border = item["_id"]["border"]
        count = item["count"]
        if border not in output:
            output[border] = {}
        output[border] = count

    return output


def get_top_urgent_zones():
    # find top 5 zones with most URGENT
    pipeline = [
        {"$match": {"priority": "URGENT"}},
        {
            "$group": {
                "_id": "$zone",
                "urgent_count": {"$sum": 1}
            }
        },
        {"$sort": {"urgent_count": -1}},
        {"$limit": 5}
    ]
    results = list(collection.aggregate(pipeline))

    return [
        {"zone": item["_id"], "urgent_count": item["urgent_count"]}
        for item in results
    ]


def get_distance_distribution():
    # distribute alerts into distance ranges from fence
    pipeline = [
        # TODO: I DONT REMEBE HOW TO DO THIS THIS IS PSUEDOCODE
        {
            "$bucket": {
                "groupBy": "$distance_from_fence_m",
                "boundaries": [0, 300, 800],
                "output": {
                    "count": {"$sum": 1}
                }
            }
        }
    ]
    results = list(collection.aggregate(pipeline))

    labels = {
        0: " close: 0-300m",
        300: "medium: 300-800m",
        800: "far: 800-1500m+",
    }

    return [
        {
            "range": labels.get(item["_id"], str(item["_id"])),
            "count": item["count"]
        }
        for item in results
    ]


def get_low_visibility_high_activity():
    # find zones with high people count and low visibility 
    pipeline = [
        {
            "$match": {
                # 0.4 and under visibility
                "visibility_quality": {"$lte": 0.4},
                # avg people
                "people_count": {"$gte": {"$avg": "$people_count"}}
            }
        },
        {
            "$group": {
                "_id": "$zone",
            }
        },
    ]
    results = list(collection.aggregate(pipeline))

    return [
        {
            "zone": item["_id"],
            "alert_count": item["alert_count"],
            "avg_people_count": round(item["avg_people_count"], 2),
            "avg_visibility": round(item["avg_visibility"], 2)
        }
        for item in results
    ]


def get_hot_zones():
    # find zones with high urgent count and low average distance from fence
    pass
