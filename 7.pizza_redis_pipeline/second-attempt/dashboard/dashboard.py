"""
Streamlit Dashboard - Pizza Operations Monitor

INPUT:
    - reads all orders from MongoDB (direct query)
    - optionally reads cached metrics from Redis key "dashboard:metrics" (TTL 30s)

OUTPUT:
    - Pie Chart: order status distribution (PREPARING, DELIVERED, BURNT, CANCELLED)
      shows total order count in the title
    - Bar Chart: top 10 allergens that caused CANCELLED orders
    - Table: last 10 orders processed (sorted by update_time desc)
    - Cache indicator: shows whether data came from Redis or MongoDB

FLOW:
    Redis (cache check) -> MongoDB (fallback/fresh data) -> Streamlit UI
    User reloads page to refresh data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pymongo import MongoClient
import os
from dotenv import dotenv_values
import redis

# --- Config ---
ENV = {**dotenv_values(".env.local"), **os.environ}
MONGO_URI = ENV.get("MONGO_URI", "mongodb://127.0.0.1:27017/")
MONGO_DB = ENV.get("MONGO_DB", "pizza_mongo")
REDIS_HOST = ENV.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(ENV.get("REDIS_PORT", "6379"))
REDIS_PASSWORD = ENV.get("REDIS_PASSWORD", "") or None

# --- Connections ---
mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = mongo_client[MONGO_DB]
collection = db["pizza_orders"]

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True,
)


def get_cached_metrics():
    """Try to get pre-computed metrics from Redis cache."""
    try:
        cached = r.get("dashboard:metrics")
        if cached:
            return json.loads(cached), True
    except Exception:
        pass
    return None, False


def compute_metrics_from_mongo():
    """Compute all dashboard metrics directly from MongoDB."""
    orders = list(collection.find({}, {"_id": 0}))
    if not orders:
        return None
    df = pd.DataFrame(orders)
    return df


# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Pizza Operations Dashboard",
    layout="wide"
)

st.title("Pizza Operations Dashboard")

# Check Redis cache first
cached_data, cache_hit = get_cached_metrics()
if cache_hit:
    st.caption("Data source: Redis Cache (fast)")
else:
    st.caption("Data source: MongoDB (fresh query)")

# --- Load data ---
df = compute_metrics_from_mongo()

if df is None or df.empty:
    st.warning("No orders found in MongoDB.")
    st.stop()

# --- Total Orders ---
total_orders = len(df)

# =============================
# ROW 1: Pie Chart + Stats
# =============================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Order Status Distribution")

    if "status" in df.columns:
        status_counts = df["status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]

        fig_pie = px.pie(
            status_counts,
            names="status",
            values="count",
            title=f"Status Distribution (Total Orders: {total_orders})",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No status data available.")

with col2:
    st.subheader("Summary")
    st.metric("Total Orders", total_orders)

    if "status" in df.columns:
        for status, count in df["status"].value_counts().items():
            st.metric(status, count)

# =============================
# ROW 2: Top 10 Allergens Bar Chart
# =============================
st.subheader("Top 10 Allergens (from CANCELLED orders)")

if "allergens_matched" in df.columns and "status" in df.columns:
    cancelled_df = df[df["status"] == "CANCELLED"].copy()

    if not cancelled_df.empty:
        # explode the allergens_matched lists into individual rows
        allergens_series = cancelled_df["allergens_matched"].dropna()

        # handle both list and string types
        all_allergens = []
        for item in allergens_series:
            if isinstance(item, list):
                all_allergens.extend(item)
            elif isinstance(item, str):
                all_allergens.append(item)

        if all_allergens:
            allergen_counts = pd.Series(all_allergens).value_counts().head(10).reset_index()
            allergen_counts.columns = ["allergen", "count"]

            fig_bar = px.bar(
                allergen_counts,
                x="allergen",
                y="count",
                title="Top 10 Allergens Causing Cancellations",
                color="count",
                color_continuous_scale="Reds"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No allergen data found in cancelled orders.")
    else:
        st.info("No CANCELLED orders found.")
else:
    st.info("No allergens_matched data available yet. Run the Risk Evaluator first.")

# =============================
# ROW 3: Last 10 Orders Table
# =============================
st.subheader("Last 10 Orders Processed")

if "update_time" in df.columns:
    recent_df = df.dropna(subset=["update_time"]).sort_values("update_time", ascending=False).head(10)

    # select display columns
    display_cols = ["order_id", "pizza_type", "status", "allergens_matched", "update_time"]
    available_cols = [c for c in display_cols if c in recent_df.columns]

    if not recent_df.empty:
        st.dataframe(
            recent_df[available_cols].reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No orders with update_time found yet.")
else:
    st.info("No update_time data available yet. Run the Risk Evaluator first.")

# --- Footer ---
st.markdown("---")
st.caption(f"Cache status: {'HIT' if cache_hit else 'MISS'} | Auto-refresh: reload page")

# streamlit run dashboard/dashboard.py
