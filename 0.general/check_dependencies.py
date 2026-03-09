"""
check_dependencies.py
---------------------
Checks that the key Python libraries required for THIS project are installed and
minimally functional.

Safe by default:
- No external network calls (Mongo/MySQL/Kafka) unless enabled.

Usage
-----
1) Activate venv:
   source venv/Scripts/activate   (Git Bash on Windows)

2) Run:
   python check_dependencies.py

Optional: run network checks (requires running services + correct .env):
   RUN_NETWORK_TESTS=true python check_dependencies.py
"""

import os
import traceback
from pathlib import Path

# -------------------------------------------------
# Optional: enable network checks (disabled by default)
# -------------------------------------------------
RUN_NETWORK_TESTS = os.getenv("RUN_NETWORK_TESTS", "false").lower() == "true"

# -------------------------------------------------
# Pip install hints (what to install when a test fails due to missing import)
# -------------------------------------------------
PIP_INSTALL_HINTS = {
    "FastAPI": "fastapi",
    "Uvicorn": "uvicorn[standard]",
    "Requests": "requests",
    "Pydantic": "pydantic",
    # For EmailStr validation dependency:
    # (You can also use: email-validator)
    "email_validator": 'pydantic[email]',
    "motor": "motor",
    "beanie": "beanie",
    "mysql-connector-python": "mysql-connector-python",
    "confluent-kafka": "confluent-kafka",
    "python-dotenv": "python-dotenv",
}

# -------------------------------------------------
# What to test (project-focused)
# -------------------------------------------------
TEST_LIBRARIES = {
    "Standard Library": {
        "os": True,
        "sys": True,
        "json": True,
        "datetime": True,
        "pathlib": True,
        "logging": True,
    },
    "Web/API": {
        "FastAPI": True,
        "Uvicorn": True,
        "Requests": True,
    },
    "Validation": {
        "Pydantic": True,
        "email_validator": True,  # explicit dependency for EmailStr
    },
    "Mongo (Beanie + Motor)": {
        "motor": True,
        "beanie": True,
    },
    "MySQL": {
        "mysql-connector-python": True,
    },
    "Kafka": {
        "confluent-kafka": True,
    },
    "Env/Config": {
        "python-dotenv": True,
        "configparser": True,
    },
}

# -------------------------------------------------
# Store results
# -------------------------------------------------
results = {}
errors = {}
missing_pip_installs = set()


def _mark_missing_install(test_name: str, exc: Exception) -> None:
    """
    Only suggest pip install when it looks like an import/dependency problem.
    """
    if isinstance(exc, (ModuleNotFoundError, ImportError)):
        hint = PIP_INSTALL_HINTS.get(test_name)
        if hint:
            missing_pip_installs.add(hint)


def test_import(name, func):
    print(f"\n=== Testing {name} ===")
    try:
        func()
        print(f"[PASS] {name} works")
        results[name] = True
    except Exception as e:
        print(f"[FAIL] {name} error:")
        print(type(e).__name__, e)
        traceback.print_exc()

        results[name] = False
        errors[name] = f"{type(e).__name__}: {e}"

        _mark_missing_install(name, e)


# -------------------------------------------------
# Test functions
# -------------------------------------------------
def test_fastapi():
    from fastapi import FastAPI

    app = FastAPI()
    assert callable(app.get)


def test_uvicorn():
    import uvicorn

    assert hasattr(uvicorn, "run")


def test_requests():
    import requests

    r = requests.Response()
    assert isinstance(r, requests.Response)


def test_pydantic_and_emailstr():
    from pydantic import BaseModel, EmailStr

    class T(BaseModel):
        email: EmailStr

    # This will fail if `email-validator` / `pydantic[email]` is missing
    T(email="test@example.com")


def test_email_validator():
    from email_validator import validate_email

    res = validate_email("test@example.com", check_deliverability=False)
    assert res.email == "test@example.com"


def test_motor():
    from motor.motor_asyncio import AsyncIOMotorClient

    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(mongo_uri)
    assert client is not None

    # Optional real ping
    if RUN_NETWORK_TESTS:
        import asyncio

        async def ping():
            await client.admin.command({"ping": 1})

        asyncio.run(ping())

    client.close()


def test_beanie():
    from beanie import Document
    from pydantic import Field

    class Demo(Document):
        name: str = Field(min_length=1)

    d = Demo(name="ok")
    assert d.name == "ok"


def test_mysql_connector():
    import mysql.connector

    assert hasattr(mysql.connector, "connect")

    # Optional real connect + SELECT 1
    if RUN_NETWORK_TESTS:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "127.0.0.1"),
            port=int(os.getenv("MYSQL_PORT", "3307")),
            user=os.getenv("MYSQL_USER", "app"),
            password=os.getenv("MYSQL_PASSWORD", "app_pw"),
            database=os.getenv("MYSQL_DB", "social_commerce"),
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        row = cur.fetchone()
        assert row is not None
        cur.close()
        conn.close()


def test_confluent_kafka():
    from confluent_kafka import Producer, Consumer

    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    p = Producer({"bootstrap.servers": bootstrap, "client.id": "deps-check-producer"})
    assert p is not None

    c = Consumer(
        {
            "bootstrap.servers": bootstrap,
            "group.id": "deps-check-group",
            "auto.offset.reset": "earliest",
        }
    )
    assert c is not None
    c.close()

    # Optional broker contact
    if RUN_NETWORK_TESTS:
        md = p.list_topics(timeout=3)
        assert md is not None


def test_dotenv():
    from dotenv import load_dotenv

    # Do NOT overwrite user's .env; create a temp file
    tmp = Path(".env.deps_test")
    tmp.write_text("TEST_VALUE=123\n", encoding="utf-8")

    load_dotenv(dotenv_path=tmp, override=True)
    assert os.getenv("TEST_VALUE") == "123"

    tmp.unlink(missing_ok=True)


def test_configparser():
    import configparser

    c = configparser.ConfigParser()
    c.read_dict({"section": {"key": "value"}})
    assert c["section"]["key"] == "value"


TEST_FUNCTIONS = {
    "FastAPI": test_fastapi,
    "Uvicorn": test_uvicorn,
    "Requests": test_requests,
    "Pydantic": test_pydantic_and_emailstr,
    "email_validator": test_email_validator,
    "motor": test_motor,
    "beanie": test_beanie,
    "mysql-connector-python": test_mysql_connector,
    "confluent-kafka": test_confluent_kafka,
    "python-dotenv": test_dotenv,
    "configparser": test_configparser,
}

# -------------------------------------------------
# Run
# -------------------------------------------------
if __name__ == "__main__":
    print("\n### PYTHON DEPENDENCY DIAGNOSTICS (PROJECT) ###")
    print(f"RUN_NETWORK_TESTS={RUN_NETWORK_TESTS}")

    for category, libs in TEST_LIBRARIES.items():
        print(f"\n--- Category: {category} ---")
        for name, enabled in libs.items():
            if not enabled:
                print(f"[SKIPPED] {name}")
                results[name] = None
                continue

            if name in TEST_FUNCTIONS:
                test_import(name, TEST_FUNCTIONS[name])
            else:
                print(f"\n=== Testing {name} (import only) ===")
                try:
                    __import__(name)
                    print(f"[PASS] {name} import works")
                    results[name] = True
                except Exception as e:
                    print(f"[FAIL] {name} import error:")
                    print(type(e).__name__, e)
                    traceback.print_exc()

                    results[name] = False
                    errors[name] = f"{type(e).__name__}: {e}"
                    _mark_missing_install(name, e)

    print("\n### FINAL SUMMARY ###")
    for name, status in results.items():
        state = "PASS" if status is True else "FAIL" if status is False else "SKIPPED"
        print(f"- {name}: {state}")

    passed = sum(1 for x in results.values() if x)
    total = sum(1 for x in results.values() if x is not None)
    print(f"\nOverall: {passed}/{total} tests passed")

    if errors:
        print("\n### ERRORS ###")
        for name, err in errors.items():
            print(f"- {name}: {err}")

    # -------------------------------------------------
    # Print pip install command for missing deps
    # -------------------------------------------------
    if missing_pip_installs:
        installs = sorted(missing_pip_installs)
        print("\n### INSTALL MISSING PACKAGES ###")
        print("Run this:")
        # Quote items that contain brackets
        parts = []
        for pkg in installs:
            parts.append(f'"{pkg}"' if "[" in pkg or "]" in pkg else pkg)
        print("pip install " + " ".join(parts))
    else:
        print("\nNo missing pip installs detected (based on import errors).")