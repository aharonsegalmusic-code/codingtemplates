

def classify(alert):
    # URGENT - any single one 
    if alert["weapons_count"] > 0:
        return "URGENT"
    if alert["distance_from_fence_m"] <= 50:
        return "URGENT"
    if alert["people_count"] >= 8:
        return "URGENT"
    if alert["vehicle_type"] == "truck":
        return "URGENT"

    # combined conditions
    if alert["distance_from_fence_m"] <= 150 and alert["people_count"] >= 4:
        return "URGENT"
    if alert["vehicle_type"] == "jeep" and alert["people_count"] >= 3:
        return "URGENT"

    return "NORMAL"