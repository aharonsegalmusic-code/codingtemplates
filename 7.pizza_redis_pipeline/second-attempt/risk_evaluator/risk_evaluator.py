"""
Risk Evaluator Service - "Officer of Risks"

INPUT:
    - reads orders from MongoDB (all non-CANCELLED orders)
    - reads common_allergens list from pizza_analysis_lists.json

OUTPUT:
    - loads orders into a Pandas DataFrame
    - matches clean_special_instructions against common_allergens (substring)
    - if allergen match found -> sets status to "CANCELLED" (overrides all)
    - updates allergens_matched list + update_time for all scanned orders
    - caches dashboard:metrics in Redis (TTL 30s) for the Streamlit dashboard
    - logs aggregation results to stdout (status counts, top allergens)

FLOW:
    MongoDB -> DataFrame -> allergen matching -> MongoDB (update status + update_time)
                                              -> Redis (cache dashboard metrics)
    Runs every 10 seconds in a loop.
"""

import logging
import json
import time
import pandas as pd
from datetime import datetime, timezone

from .connection.mongo_connection import mongo
from .connection.redis_connection import r

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("risk_evaluator")

# --- Load closed lists ---
with open('data/pizza_analysis_lists.json', 'r') as file:
    pizza_analysis_lists = json.load(file)

COMMON_ALLERGENS = pizza_analysis_lists["common_allergens"]

collection = mongo.collection("pizza_orders")

SCAN_INTERVAL = 10  # seconds between scans


def find_allergen_matches(clean_text: str, allergens: list) -> list:
    """
    Substring matching with case-normalization.
    Both text and allergens are converted to UPPERCASE before matching.
    Returns list of matched allergens.
    """
    if not clean_text:
        return []

    upper_text = clean_text.upper()
    matched = [allergen for allergen in allergens if allergen.upper() in upper_text]
    return matched


def scan_and_evaluate():
    """
    Main scan cycle:
    1. Pull all non-CANCELLED orders from MongoDB into DataFrame
    2. Match clean_special_instructions against common_allergens
    3. Mark CANCELLED if match found
    4. Update update_time for all scanned orders
    5. Log results
    """
    # --- 6.1 Create DataFrame ---
    orders_cursor = collection.find(
        {"status": {"$ne": "CANCELLED"}},
        {"_id": 0, "order_id": 1, "pizza_type": 1, "status": 1,
         "clean_special_instructions": 1, "insertion_time": 1, "update_time": 1}
    )
    orders_list = list(orders_cursor)

    if not orders_list:
        logger.info("No orders to scan.")
        return

    df = pd.DataFrame(orders_list)
    logger.info(f"Scan started: {len(df)} orders loaded from MongoDB.")

    # ensure clean_special_instructions column exists
    if "clean_special_instructions" not in df.columns:
        df["clean_special_instructions"] = ""
    df["clean_special_instructions"] = df["clean_special_instructions"].fillna("")

    # --- 6.2 Derived columns ---
    df["allergens_matched"] = df["clean_special_instructions"].apply(
        lambda text: find_allergen_matches(text, COMMON_ALLERGENS)
    )
    df["should_cancel"] = df["allergens_matched"].apply(lambda matches: len(matches) > 0)

    # --- Update MongoDB ---
    now = datetime.now(timezone.utc).isoformat()
    cancelled_count = 0

    for _, row in df.iterrows():
        order_id = row["order_id"]
        update_fields = {"update_time": now}

        if row["should_cancel"]:
            # CANCELLED overrides all other statuses
            update_fields["status"] = "CANCELLED"
            update_fields["allergens_matched"] = row["allergens_matched"]
            cancelled_count += 1
            logger.info(
                f"[CANCELLED] order_id={order_id} | "
                f"allergens_matched={row['allergens_matched']}"
            )

        collection.update_one(
            {"order_id": order_id},
            {"$set": update_fields}
        )

    logger.info(f"Scan complete: {cancelled_count} orders marked CANCELLED out of {len(df)} scanned.")

    # --- 6.3 Aggregations ---
    # counts by status
    status_counts = df["status"].value_counts()
    logger.info(f"Status counts (pre-update snapshot):\n{status_counts.to_string()}")

    # Top 10 allergens that caused cancellations
    cancelled_df = df[df["should_cancel"]]
    if not cancelled_df.empty:
        all_allergens = cancelled_df["allergens_matched"].explode()
        top_allergens = all_allergens.value_counts().head(10)
        logger.info(f"Top allergens (this scan):\n{top_allergens.to_string()}")
    else:
        logger.info("No allergen matches found in this scan.")

    # --- Optional: cache aggregation results in Redis ---
    try:
        # refresh status counts from mongo after updates
        all_orders = list(collection.find({}, {"_id": 0, "order_id": 1, "status": 1,
                                                "allergens_matched": 1, "update_time": 1,
                                                "pizza_type": 1}))
        all_df = pd.DataFrame(all_orders)

        fresh_status_counts = all_df["status"].value_counts().to_dict() if "status" in all_df.columns else {}

        # top allergens from all CANCELLED orders
        if "allergens_matched" in all_df.columns:
            cancelled_all = all_df[all_df.get("status") == "CANCELLED"]
            if not cancelled_all.empty and "allergens_matched" in cancelled_all.columns:
                all_matched = cancelled_all["allergens_matched"].dropna().explode()
                top_all = all_matched.value_counts().head(10).to_dict()
            else:
                top_all = {}
        else:
            top_all = {}

        # last 10 orders by update_time
        if "update_time" in all_df.columns:
            sorted_df = all_df.dropna(subset=["update_time"]).sort_values("update_time", ascending=False).head(10)
            last_10 = sorted_df["order_id"].tolist()
        else:
            last_10 = []

        cache_data = {
            "status_counts": fresh_status_counts,
            "top_allergens": top_all,
            "last_10_orders": last_10
        }
        r.set("dashboard:metrics", json.dumps(cache_data), ex=30)
        logger.info("Dashboard metrics cached in Redis (TTL=30s).")
    except Exception as e:
        logger.warning(f"Redis cache update failed: {e}")


def main():
    logger.info("Risk Evaluator started. Scanning every %d seconds.", SCAN_INTERVAL)
    while True:
        try:
            scan_and_evaluate()
        except Exception as e:
            logger.error(f"Error during scan: {e}")
        time.sleep(SCAN_INTERVAL)


main()

# python -m risk_evaluator.risk_evaluator
