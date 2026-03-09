# general/healthcheck.py
"""
One-file healthcheck for this project (Mongo + MySQL + optional Docker + optional API).

What it does:
1) Prints copy/paste CLI commands (docker exec) for Mongo + MySQL
2) Runs real connection tests from your host Python:
   - MongoDB: ping
   - MySQL: SELECT 1
3) (Optional) Checks Docker containers are running
4) (Optional) Checks FastAPI /docs is reachable

Run:
  python general/healthcheck.py

Common options:
  python general/healthcheck.py --print-only
  python general/healthcheck.py --test-only
  python general/healthcheck.py --no-docker
  python general/healthcheck.py --no-api
"""

from __future__ import annotations

import argparse
import asyncio
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
import mysql.connector


# =========================
# CONFIG (edit these only)
# =========================

# --- Docker container names (CHANGE if you renamed containers in docker-compose.yml)
MONGO_CONTAINER = "sc_mongo"   # usually change if container_name differs
MYSQL_CONTAINER = "sc_mysql"   # usually change if container_name differs

# --- MongoDB (HOST -> Docker published port)
MONGO_HOST = "127.0.0.1"       # change if Mongo is on another machine
MONGO_PORT = 27017             # change if you mapped to a different host port
MONGO_DB = "social_commerce"   # change if you use a different DB name
MONGO_TIMEOUT_MS = 2000        # change if your machine is slow / you want longer timeout

# Mongo auth (CHANGE if you enabled auth / credentials differ)
MONGO_AUTH_ENABLED = False     # common change: set True when auth is enabled
MONGO_USER = "app"             # common change: match MONGO_INITDB_ROOT_USERNAME (or your app user)
MONGO_PASSWORD = "app_pw"      # common change: match MONGO_INITDB_ROOT_PASSWORD (or your app user password)
MONGO_AUTHSOURCE = "admin"     # common change: usually "admin" for root user

# --- MySQL (HOST -> Docker published port)
MYSQL_HOST = "127.0.0.1"       # change if MySQL is on another machine
MYSQL_PORT = 3307              # VERY common change on Windows (3306 often already used)
MYSQL_DB = "social_commerce"   # change if you use a different DB name
MYSQL_USER = "app"             # common change: use "app" (avoid root unless needed)
MYSQL_PASSWORD = "app_pw"      # common change: match MYSQL_PASSWORD

# --- Optional: FastAPI check (CHANGE if your API runs on another port/host)
API_CHECK_ENABLED = True       # set False if you only care about DB checks
API_BASE_URL = "http://127.0.0.1:8000"  # common change: port 8000 -> something else
API_PATH = "/docs"             # common change: "/health" if you add a health endpoint


# =========================
# Models / helpers
# =========================

@dataclass
class CheckResult:
    name: str
    ok: bool
    details: str


def build_mongo_uri() -> str:
    if not MONGO_AUTH_ENABLED:
        return f"mongodb://{MONGO_HOST}:{MONGO_PORT}"
    return (
        f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}"
        f"@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
        f"?authSource={MONGO_AUTHSOURCE}"
    )


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def _print_section(title: str) -> None:
    print("\n" + "=" * len(title))
    print(title)
    print("=" * len(title))


# =========================
# CLI command generator
# =========================

def cli_commands() -> dict[str, str]:
    cmds: dict[str, str] = {}

    # MySQL
    cmds["MySQL: SELECT 1 (docker exec)"] = (
        f'docker exec -it {MYSQL_CONTAINER} '
        f'mysql -u{MYSQL_USER} -p{MYSQL_PASSWORD} -D {MYSQL_DB} '
        f'-e "SELECT 1;"'
    )

    # Mongo
    cmds["Mongo: ping (NO auth)"] = (
        f'docker exec -it {MONGO_CONTAINER} '
        f'mongosh --quiet --eval "db.runCommand({{ ping: 1 }})"'
    )

    cmds["Mongo: ping (WITH auth)"] = (
        f'docker exec -it {MONGO_CONTAINER} '
        f'mongosh --quiet -u {MONGO_USER} -p {MONGO_PASSWORD} '
        f'--authenticationDatabase {MONGO_AUTHSOURCE} '
        f'--eval "db.runCommand({{ ping: 1 }})"'
    )

    cmds["Mongo: show dbs (NO auth)"] = (
        f'docker exec -it {MONGO_CONTAINER} '
        f'mongosh --quiet --eval "show dbs"'
    )

    cmds["Mongo: show dbs (WITH auth)"] = (
        f'docker exec -it {MONGO_CONTAINER} '
        f'mongosh --quiet -u {MONGO_USER} -p {MONGO_PASSWORD} '
        f'--authenticationDatabase {MONGO_AUTHSOURCE} '
        f'--eval "show dbs"'
    )

    return cmds


def print_cli_commands() -> None:
    _print_section("CLI commands (copy/paste)")
    print("# Use the *auth* Mongo commands only if your Mongo enforces authentication.\n")
    for title, cmd in cli_commands().items():
        print(f"# {title}\n{cmd}\n")


# =========================
# Actual tests
# =========================

async def test_mongo() -> CheckResult:
    name = "MongoDB ping"
    uri = build_mongo_uri()
    try:
        client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=MONGO_TIMEOUT_MS)
        await client.admin.command("ping")
        return CheckResult(name, True, f"OK -> {uri}")
    except Exception as e:
        return CheckResult(name, False, f"{type(e).__name__}: {e} (uri={uri})")


def test_mysql() -> CheckResult:
    name = "MySQL SELECT 1"
    try:
        db = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
        )
        cur = db.cursor()
        cur.execute("SELECT 1")
        val = cur.fetchone()[0]
        cur.close()
        db.close()
        return CheckResult(name, True, f"OK -> {MYSQL_HOST}:{MYSQL_PORT} as {MYSQL_USER} (SELECT 1 = {val})")
    except Exception as e:
        return CheckResult(name, False, f"{type(e).__name__}: {e} (host={MYSQL_HOST}:{MYSQL_PORT}, user={MYSQL_USER})")


def test_docker_container_running(container_name: str) -> CheckResult:
    name = f"Docker container running: {container_name}"
    try:
        cp = _run(["docker", "inspect", "-f", "{{.State.Running}}", container_name])
        if cp.returncode != 0:
            return CheckResult(name, False, f"docker inspect failed: {cp.stderr.strip() or cp.stdout.strip()}")
        running = (cp.stdout.strip().lower() == "true")
        return CheckResult(name, running, "OK" if running else "Not running")
    except FileNotFoundError:
        return CheckResult(name, False, "docker command not found (is Docker installed / in PATH?)")
    except Exception as e:
        return CheckResult(name, False, f"{type(e).__name__}: {e}")


def test_api_docs() -> CheckResult:
    """
    No external deps: uses stdlib urllib.
    """
    name = "FastAPI reachable (/docs)"
    url = f"{API_BASE_URL.rstrip('/')}{API_PATH}"
    try:
        import urllib.request
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=2) as resp:
            code = resp.getcode()
        ok = 200 <= code < 400
        return CheckResult(name, ok, f"HTTP {code} -> {url}")
    except Exception as e:
        return CheckResult(name, False, f"{type(e).__name__}: {e} (url={url})")


def print_results(results: list[CheckResult]) -> None:
    _print_section("Test results")
    ok_count = 0
    for r in results:
        status = "OK " if r.ok else "FAIL"
        print(f"[{status}] {r.name}\n  {r.details}\n")
        ok_count += int(r.ok)

    print(f"Summary: {ok_count}/{len(results)} checks OK")
    if ok_count != len(results):
        print("Fix the FAIL items first; they usually explain why seeding/app flows break.")


# =========================
# Main
# =========================

async def run_tests(enable_docker: bool, enable_api: bool) -> list[CheckResult]:
    results: list[CheckResult] = []

    if enable_docker:
        results.append(test_docker_container_running(MONGO_CONTAINER))
        results.append(test_docker_container_running(MYSQL_CONTAINER))

    results.append(await test_mongo())
    results.append(test_mysql())

    if enable_api and API_CHECK_ENABLED:
        results.append(test_api_docs())

    return results


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--print-only", action="store_true", help="Only print CLI commands (no tests).")
    p.add_argument("--test-only", action="store_true", help="Only run tests (no CLI commands).")
    p.add_argument("--no-docker", action="store_true", help="Skip docker container running checks.")
    p.add_argument("--no-api", action="store_true", help="Skip FastAPI /docs check.")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    do_print = not args.test_only
    do_test = not args.print_only

    if do_print:
        print_cli_commands()

    if do_test:
        results = asyncio.run(run_tests(enable_docker=not args.no_docker, enable_api=not args.no_api))
        print_results(results)


if __name__ == "__main__":
    main()