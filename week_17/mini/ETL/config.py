import os

# -----------------------------
# ENV (minimal, defaults match your project)
# -----------------------------
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://app:app_pw@127.0.0.1:27017/social_commerce?authSource=admin",
)
MONGO_DB = os.getenv("MONGO_DB", "social_commerce")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "mini_users")  # <- your Beanie collection name

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3307"))
MYSQL_DB = os.getenv("MYSQL_DB", "social_commerce")
MYSQL_USER = os.getenv("MYSQL_USER", "app")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "app_pw")

ETL_BATCH_SIZE = int(os.getenv("ETL_BATCH_SIZE", "50"))
ETL_POLL_SECONDS = int(os.getenv("ETL_POLL_SECONDS", "5"))

STATE_KEY = os.getenv("ETL_STATE_KEY", "mongo_to_mysql_users")  # identifies this ETL job