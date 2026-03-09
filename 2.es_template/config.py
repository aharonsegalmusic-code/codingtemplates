# config.py
# ─────────────────────────────────────────────────────────────
import os
from dotenv import load_dotenv   # reads the .env file into os.environ

load_dotenv()

# ── Elasticsearch ────────────────────────────────────────────
ES_HOST  = os.getenv("ES_HOST",  "http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX", "pizza_orders")

# ── Data ─────────────────────────────────────────────────────
DATA_FILE = os.getenv("DATA_FILE", "data/pizza_orders.json")

# ── FastAPI ──────────────────────────────────────────────────
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
