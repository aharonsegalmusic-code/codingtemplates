# compose_to_env.py
#
# Reads a docker-compose file and generates TWO env files:
# - .env.local  (for running apps on your PC  → 127.0.0.1 + published ports)
# - .env.docker (for running apps in Docker   → service names + container ports)
#
# 100% dynamic — reads exactly what's in your compose, no hardcoded values.
#
# install:
#   pip install pyyaml
#
# run:
#   python compose_to_env.py
#   python compose_to_env.py --compose docker-compose.yml
#   python compose_to_env.py --also-dotenv local

from __future__ import annotations

import argparse
import re
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Tuple

import yaml

COMPOSE_PATH = "docker-compose.yml"

# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------

def _as_str(x: Any) -> str:
    return "" if x is None else str(x)


def image_of(svc: Dict[str, Any]) -> str:
    return _as_str(svc.get("image", "")).lower()


def get_env_map(svc: Dict[str, Any]) -> Dict[str, str]:
    """Extract environment variables from a service definition."""
    env = svc.get("environment", {}) or {}
    out: Dict[str, str] = {}
    if isinstance(env, dict):
        for k, v in env.items():
            out[_as_str(k)] = _as_str(v)
    elif isinstance(env, list):
        for item in env:
            if isinstance(item, str) and "=" in item:
                k, v = item.split("=", 1)
                out[k.strip()] = v.strip()
    return out


def parse_port_mapping(port_str: str) -> Optional[Tuple[int, int]]:
    """
    "18081:8081"            → (18081, 8081)
    "127.0.0.1:18081:8081"  → (18081, 8081)
    "18081:8081/tcp"        → (18081, 8081)
    """
    s = port_str.strip().split("/")[0]
    parts = s.split(":")
    if len(parts) == 2:
        host_p, cont_p = parts
    elif len(parts) == 3:
        _, host_p, cont_p = parts
    else:
        return None
    try:
        return int(host_p), int(cont_p)
    except ValueError:
        return None


def get_all_port_mappings(svc: Dict[str, Any]) -> List[Tuple[int, int]]:
    """Return all (host_port, container_port) pairs for a service."""
    ports = svc.get("ports", []) or []
    out = []
    for p in ports:
        if isinstance(p, str):
            m = parse_port_mapping(p)
            if m:
                out.append(m)
        elif isinstance(p, dict):
            published = p.get("published")
            target = p.get("target")
            if published and target:
                try:
                    out.append((int(published), int(target)))
                except ValueError:
                    pass
    return out


def get_host_port(svc: Dict[str, Any], container_port: int) -> Optional[int]:
    for host_p, cont_p in get_all_port_mappings(svc):
        if cont_p == container_port:
            return host_p
    return None


# ---------------------------------------------------------------------------
#  Value rewriter: docker-internal → local (127.0.0.1 + host ports)
# ---------------------------------------------------------------------------

def _resolve_unpublished_port(svc: Dict[str, Any], internal_port: int) -> int:
    """
    When an internal port isn't directly published (e.g. kafka 29092),
    find the first published port on the service as the host-facing alternative.
    For Kafka specifically: apps use 29092 internally, but localhost uses 9092.
    """
    mappings = get_all_port_mappings(svc)
    if mappings:
        # return the first published host port
        return mappings[0][0]
    return internal_port


def _rewrite_value_to_local(
    value: str,
    service_names: set[str],
    services: Dict[str, Any],
) -> str:
    """
    Rewrites service hostnames → 127.0.0.1 with published host ports.

    Handles:
      scheme://host:port/path  →  scheme://127.0.0.1:host_port/path
      host:port                →  127.0.0.1:host_port
      host:port,host2:port2    →  127.0.0.1:hp1,127.0.0.1:hp2
    """

    # --- pattern 1: scheme://host:port[/path] ---
    url_match = re.match(r'^(\w+)://([\w._-]+):(\d+)(.*)', value)
    if url_match:
        scheme, host, port_str, rest = url_match.groups()
        port = int(port_str)
        if host in service_names:
            svc_def = services.get(host, {})
            host_port = get_host_port(svc_def, port) or port
            return f"{scheme}://127.0.0.1:{host_port}{rest}"
        return value

    # --- pattern 2: scheme://host[/path] (no port) ---
    url_no_port = re.match(r'^(\w+)://([\w._-]+)(/.*)?$', value)
    if url_no_port:
        scheme, host, rest = url_no_port.groups()
        rest = rest or ""
        if host in service_names:
            return f"{scheme}://127.0.0.1{rest}"
        return value

    # --- pattern 3: host:port  or  host:port,host2:port2 (kafka etc.) ---
    if ":" in value and not value.startswith("/"):
        parts = value.split(",")
        rewritten = []
        changed = False
        for part in parts:
            hp_match = re.match(r'^([\w._-]+):(\d+)$', part.strip())
            if hp_match:
                host, port_str = hp_match.groups()
                port = int(port_str)
                if host in service_names:
                    svc_def = services.get(host, {})
                    host_port = get_host_port(svc_def, port)
                    if host_port:
                        rewritten.append(f"127.0.0.1:{host_port}")
                    else:
                        # port not published (e.g. kafka internal 29092)
                        # find the PLAINTEXT_HOST listener port instead
                        resolved = _resolve_unpublished_port(svc_def, port)
                        rewritten.append(f"127.0.0.1:{resolved}")
                    changed = True
                else:
                    rewritten.append(part.strip())
            else:
                rewritten.append(part.strip())
        if changed:
            return ",".join(rewritten)

    return value


# ---------------------------------------------------------------------------
#  Filters: skip infra-internal config that apps don't need
# ---------------------------------------------------------------------------

# Kafka BROKER config (not app-facing)
_KAFKA_BROKER_PREFIXES = (
    "KAFKA_NODE_ID", "KAFKA_PROCESS_ROLES", "KAFKA_CONTROLLER_",
    "KAFKA_LISTENERS", "KAFKA_ADVERTISED_LISTENERS",
    "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP", "KAFKA_INTER_BROKER_",
    "KAFKA_OFFSETS_TOPIC_", "KAFKA_TRANSACTION_",
    "KAFKA_GROUP_INITIAL_REBALANCE", "KAFKA_AUTO_CREATE_TOPICS",
    "CLUSTER_ID",
)

# UI service config (mongo-express, kafka-ui, kibana internals)
_UI_PREFIXES = (
    "ME_CONFIG_",           # mongo-express
    "KAFKA_CLUSTERS_",      # kafka-ui
    "ELASTICSEARCH_HOSTS",  # kibana pointing to ES
)

# Elasticsearch SERVER config
_ES_SERVER_PREFIXES = (
    "discovery.type", "xpack.", "ES_JAVA_OPTS",
)

# Mongo SERVER config
_MONGO_SERVER_PREFIXES = (
    "MONGO_INITDB_",
)


def _is_infra_internal(key: str) -> bool:
    """Return True if this env var is infra-internal (should not go into app envs)."""
    for prefix in (*_KAFKA_BROKER_PREFIXES, *_UI_PREFIXES,
                   *_ES_SERVER_PREFIXES, *_MONGO_SERVER_PREFIXES):
        if key == prefix or key.startswith(prefix):
            return True
    return False


# ---------------------------------------------------------------------------
#  Detect infra vs app services by image
# ---------------------------------------------------------------------------

_INFRA_IMAGE_PATTERNS = [
    "mongo:", "mongo-express", "confluentinc/", "provectuslabs/kafka-ui",
    "elasticsearch:", "docker.elastic.co/", "kibana:", "redis:",
    "mariadb:", "mysql:", "zookeeper:", "redisinsight", "cloudbeaver",
]


def _is_infra_service(svc: Dict[str, Any]) -> bool:
    """Infra services = databases, brokers, UIs (not your code)."""
    img = image_of(svc)
    return any(p in img for p in _INFRA_IMAGE_PATTERNS)


# ---------------------------------------------------------------------------
#  Main builder
# ---------------------------------------------------------------------------

def build_envs(compose_path: str) -> Tuple[OrderedDict[str, str], OrderedDict[str, str]]:
    with open(compose_path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)

    services: Dict[str, Any] = (doc.get("services") or {}) if isinstance(doc, dict) else {}
    if not services:
        raise SystemExit("No services found in compose file.")

    service_names = set(services.keys())

    local_env:  OrderedDict[str, str] = OrderedDict()
    docker_env: OrderedDict[str, str] = OrderedDict()

    # ---- collect env vars from APP services (skip infra) ----
    for svc_name, svc_def in services.items():
        if _is_infra_service(svc_def):
            continue

        env_map = get_env_map(svc_def)
        if not env_map:
            continue

        for key, value in env_map.items():
            # skip infra-internal keys that somehow ended up in an app service
            if _is_infra_internal(key):
                continue

            # if we already have this key with the same value, skip duplicate
            # if different value, keep both (prefix with service name)
            if key in docker_env:
                if docker_env[key] == value:
                    continue
                # conflict: same key, different value → prefix it
                prefixed_key = f"{svc_name.upper().replace('-', '_')}_{key}"
                docker_env[prefixed_key] = value
                local_env[prefixed_key] = _rewrite_value_to_local(
                    value, service_names, services
                )
                continue

            # docker env = exactly as in compose
            docker_env[key] = value

            # local env = rewrite hostnames → 127.0.0.1
            local_env[key] = _rewrite_value_to_local(
                value, service_names, services
            )

    # ---- add WEB UI URLs (browser → always 127.0.0.1 for both profiles) ----
    _UI_DEFAULTS: Dict[str, Tuple[str, int]] = {
        "kafka-ui":      ("KAFKA_UI_URL",      8080),
        "kafka_ui":      ("KAFKA_UI_URL",      8080),
        "mongo-express": ("MONGO_EXPRESS_URL",  8081),
        "mongo_express": ("MONGO_EXPRESS_URL",  8081),
        "kibana":        ("KIBANA_URL",         5601),
        "redisinsight":  ("REDISINSIGHT_URL",   5540),
        "redis-insight": ("REDISINSIGHT_URL",   5540),
        "cloudbeaver":   ("CLOUDBEAVER_URL",    8978),
    }

    for svc_name, (env_key, default_port) in _UI_DEFAULTS.items():
        if svc_name not in services or env_key in local_env:
            continue
        svc_def = services[svc_name]
        host_port = get_host_port(svc_def, default_port) or default_port
        url = f"http://127.0.0.1:{host_port}"
        local_env[env_key] = url
        docker_env[env_key] = url

    return local_env, docker_env


# ---------------------------------------------------------------------------
#  Writer
# ---------------------------------------------------------------------------

def write_env_file(path: str, env: OrderedDict[str, str]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        prev_prefix = None
        for k, v in env.items():
            # blank line between different variable groups
            prefix = k.split("_")[0]
            if prev_prefix is not None and prefix != prev_prefix:
                f.write("\n")
            prev_prefix = prefix
            f.write(f"{k}={v}\n")


# ---------------------------------------------------------------------------
#  CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Generate .env.local and .env.prod from a docker-compose file. "
                    "Fully dynamic — reads exactly what's in your compose."
    )
    ap.add_argument("--compose",     default=COMPOSE_PATH, help="compose yml path")
    ap.add_argument("--out-local",   default=".env.local",  help="output for local env")
    ap.add_argument("--out-docker",  default=".env.prod",   help="output for docker env")
    ap.add_argument("--also-dotenv", choices=["none", "local", "prod"], default="none",
                    help="also copy one profile to .env")
    args = ap.parse_args()

    local_env, docker_env = build_envs(args.compose)

    write_env_file(args.out_local, local_env)
    write_env_file(args.out_docker, docker_env)

    # summary
    print(f"\nwrote: {args.out_local}  ({len(local_env)} vars)")
    print(f"wrote: {args.out_docker} ({len(docker_env)} vars)")

    print(f"\n--- {args.out_local} ---")
    for k, v in local_env.items():
        print(f"  {k}={v}")

    print(f"\n--- {args.out_docker} ---")
    for k, v in docker_env.items():
        print(f"  {k}={v}")

    if args.also_dotenv == "local":
        write_env_file(".env", local_env)
        print("\nwrote: .env (← .env.local)")
    elif args.also_dotenv == "prod":
        write_env_file(".env", docker_env)
        print("\nwrote: .env (← .env.prod)")


if __name__ == "__main__":
    main()
