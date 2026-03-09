# compose_to_env.py
#
# makes TWO env files from a docker-compose file:
# - .env.local  (apps run on your PC -> use 127.0.0.1 + published ports)
# - .env.docker (apps run in Docker -> use service names + container ports)
#
# install:
#   pip install pyyaml
#
# run:
#   python compose_to_env.py
#   python compose_to_env.py --compose docker-compose.deps.yml
#
# optional:
#   python compose_to_env.py --also-dotenv local   # also writes .env = .env.local
#   python compose_to_env.py --also-dotenv docker  # also writes .env = .env.docker

from __future__ import annotations

import argparse
import re
from collections import OrderedDict
from typing import Any, Dict, Optional, Tuple

import yaml

# change this if you want a default without typing flags
COMPOSE_PATH = "docker-compose.deps.yml"


def _as_str(x: Any) -> str:
    return "" if x is None else str(x)


def image_of(service_def: Dict[str, Any]) -> str:
    return _as_str(service_def.get("image", "")).lower()


def get_env_map(service_def: Dict[str, Any]) -> Dict[str, str]:
    env = service_def.get("environment", {}) or {}
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


def parse_ports(service_def: Dict[str, Any]) -> list[str]:
    ports = service_def.get("ports", []) or []
    out: list[str] = []
    if isinstance(ports, list):
        for p in ports:
            if isinstance(p, str):
                out.append(p)
            elif isinstance(p, dict):
                published = p.get("published")
                target = p.get("target")
                proto = p.get("protocol", "")
                if published and target:
                    s = f"{published}:{target}"
                    if proto:
                        s += f"/{proto}"
                    out.append(s)
    return out


def parse_port_mapping(port_str: str) -> Optional[Tuple[int, int]]:
    """
    Accepts:
      "18081:8081"
      "127.0.0.1:18081:8081"
      "18081:8081/tcp"
    Returns: (host_port, container_port)
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


def get_host_port(services: Dict[str, Any], service_name: str, container_port: int) -> Optional[int]:
    sd = services.get(service_name, {})
    for p in parse_ports(sd):
        m = parse_port_mapping(p)
        if not m:
            continue
        host_p, cont_p = m
        if cont_p == container_port:
            return host_p
    return None


def select_service(
    services: Dict[str, Any],
    preferred_names: list[str],
    image_contains_any: list[str],
) -> Optional[str]:
    for n in preferred_names:
        if n in services:
            return n
    for name, sd in services.items():
        img = image_of(sd)
        if any(sub in img for sub in image_contains_any):
            return name
    return None


def _extract_port_from_listeners(listeners: str, key: str) -> Optional[int]:
    if not listeners:
        return None
    m = re.search(rf"{re.escape(key)}://[^:,]+:(\d+)", listeners)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None


def infer_kafka_ports(kafka_env: Dict[str, str], kafka_def: Dict[str, Any]) -> Tuple[int, int]:
    """
    Returns:
      (docker_internal_port, container_host_listener_port)
    Typical:
      docker_internal_port=29092
      container_host_listener_port=9092
    """
    internal = 29092
    host_listener = 9092

    adv = kafka_env.get("KAFKA_ADVERTISED_LISTENERS", "")
    m_internal = re.search(r"kafka:(\d+)", adv)
    if m_internal:
        try:
            internal = int(m_internal.group(1))
        except ValueError:
            pass

    listeners = kafka_env.get("KAFKA_LISTENERS", "")
    hl = _extract_port_from_listeners(listeners, "PLAINTEXT_HOST")
    if hl:
        host_listener = hl

    # hint from exposed container ports
    cont_ports: list[int] = []
    for p in parse_ports(kafka_def):
        m = parse_port_mapping(p)
        if m:
            cont_ports.append(m[1])

    if 29092 in cont_ports:
        internal = 29092
    if 9092 in cont_ports:
        host_listener = 9092

    return internal, host_listener


def mongo_uri(host: str, port: int, user: str, pwd: str) -> str:
    if user and pwd:
        return f"mongodb://{user}:{pwd}@{host}:{port}/?authSource=admin"
    return f"mongodb://{host}:{port}"


def write_env_file(path: str, env: "OrderedDict[str, str]") -> None:
    with open(path, "w", encoding="utf-8") as f:
        prev_prefix = None
        for k, v in env.items():
            # add blank line between different service blocks
            prefix = k.split("_")[0]
            if prev_prefix is not None and prefix != prev_prefix:
                f.write("\n")
            prev_prefix = prefix
            f.write(f"{k}={v}\n")


def build_envs(compose_path: str) -> Tuple["OrderedDict[str, str]", "OrderedDict[str, str]"]:
    with open(compose_path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)

    services: Dict[str, Any] = (doc.get("services") or {}) if isinstance(doc, dict) else {}
    if not services:
        raise SystemExit("No services found in compose file.")

    # ---- detect services ----
    mongo_svc       = select_service(services, ["mongo", "mongodb"],                            ["mongo:"])
    mysql_svc       = select_service(services, ["mysql", "mariadb"],                            ["mysql:", "mariadb:"])
    redis_svc       = select_service(services, ["redis"],                                       ["redis:"])
    kafka_svc       = select_service(services, ["kafka"],                                       ["kafka"])
    elastic_svc     = select_service(services, ["elasticsearch", "elastic"],                    ["elasticsearch:"])
    streamlit_svc   = select_service(services, ["streamlit"],                                   ["streamlit"])

    # ---- detect UI services ----
    mongo_express_svc  = select_service(services, ["mongo-express", "mongo_express"],            ["mongo-express"])
    cloudbeaver_svc    = select_service(services, ["cloudbeaver"],                               ["cloudbeaver"])
    kafka_ui_svc       = select_service(services, ["kafka-ui", "kafka_ui"],                      ["kafka-ui", "provectuslabs/kafka-ui"])
    redisinsight_svc   = select_service(services, ["redisinsight", "redis-insight", "redis_insight"], ["redisinsight", "redis/redisinsight"])
    kibana_svc         = select_service(services, ["kibana"],                                    ["kibana"])

    # ---- detect app services (FastAPI etc.) ----
    ingestion_svc  = select_service(services, ["ingestion_service", "ingestion-service"],        ["ingestion"])
    gridfs_svc     = select_service(services, ["GridFS_service", "gridfs_service", "gridfs-service"], ["gridfs"])

    local_env:  "OrderedDict[str, str]" = OrderedDict()
    docker_env: "OrderedDict[str, str]" = OrderedDict()

    # ================================================================
    #  MONGO
    # ================================================================
    if mongo_svc:
        mongo_def = services[mongo_svc]
        menv = get_env_map(mongo_def)
        user = menv.get("MONGO_INITDB_ROOT_USERNAME", "")
        pwd  = menv.get("MONGO_INITDB_ROOT_PASSWORD", "")
        db   = menv.get("MONGO_INITDB_DATABASE", "suspicious")

        host_port = get_host_port(services, mongo_svc, 27017) or 27017

        local_env["MONGO_URI"]        = mongo_uri("127.0.0.1", host_port, user, pwd)
        local_env["MONGO_DB"]         = db
        local_env["MONGO_COLLECTION"] = "records"

        docker_env["MONGO_URI"]        = mongo_uri(mongo_svc, 27017, user, pwd)
        docker_env["MONGO_DB"]         = db
        docker_env["MONGO_COLLECTION"] = "records"

    # ================================================================
    #  MYSQL / MARIADB
    # ================================================================
    if mysql_svc:
        mysql_def = services[mysql_svc]
        senv = get_env_map(mysql_def)

        db       = senv.get("MYSQL_DATABASE", "suspicious")
        root_pwd = senv.get("MYSQL_ROOT_PASSWORD", "")

        host_port = get_host_port(services, mysql_svc, 3306) or 3306

        local_env["MYSQL_HOST"]     = "127.0.0.1"
        local_env["MYSQL_PORT"]     = str(host_port)
        local_env["MYSQL_USER"]     = "root"
        local_env["MYSQL_PASSWORD"] = root_pwd
        local_env["MYSQL_DB"]       = db

        docker_env["MYSQL_HOST"]     = mysql_svc
        docker_env["MYSQL_PORT"]    = "3306"
        docker_env["MYSQL_USER"]    = "root"
        docker_env["MYSQL_PASSWORD"] = root_pwd
        docker_env["MYSQL_DB"]      = db

    # ================================================================
    #  REDIS
    # ================================================================
    if redis_svc:
        redis_def = services[redis_svc]
        renv = get_env_map(redis_def)

        # some redis images accept REDIS_PASSWORD via env or --requirepass in command
        password = renv.get("REDIS_PASSWORD", "")
        if not password:
            cmd = _as_str(redis_def.get("command", ""))
            m = re.search(r"--requirepass\s+(\S+)", cmd)
            if m:
                password = m.group(1)

        host_port = get_host_port(services, redis_svc, 6379) or 6379

        local_env["REDIS_HOST"]     = "127.0.0.1"
        local_env["REDIS_PORT"]     = str(host_port)
        local_env["REDIS_PASSWORD"] = password
        local_env["REDIS_URL"]      = f"redis://127.0.0.1:{host_port}"

        docker_env["REDIS_HOST"]     = redis_svc
        docker_env["REDIS_PORT"]     = "6379"
        docker_env["REDIS_PASSWORD"] = password
        docker_env["REDIS_URL"]      = f"redis://{redis_svc}:6379"

    # ================================================================
    #  KAFKA
    # ================================================================
    if kafka_svc:
        kafka_def = services[kafka_svc]
        kenv = get_env_map(kafka_def)
        internal_port, host_listener_port = infer_kafka_ports(kenv, kafka_def)

        published = get_host_port(services, kafka_svc, host_listener_port) or host_listener_port

        local_env["KAFKA_BOOTSTRAP_SERVERS"] = f"127.0.0.1:{published}"
        local_env["KAFKA_TOPIC"]             = "raw-records"
        local_env["KAFKA_GROUP_ID"]          = "mysql-loader"

        docker_env["KAFKA_BOOTSTRAP_SERVERS"] = f"{kafka_svc}:{internal_port}"
        docker_env["KAFKA_TOPIC"]             = "raw-records"
        docker_env["KAFKA_GROUP_ID"]          = "mysql-loader"

    # ================================================================
    #  ELASTICSEARCH
    # ================================================================
    if elastic_svc:
        elastic_def = services[elastic_svc]
        eenv = get_env_map(elastic_def)

        host_port = get_host_port(services, elastic_svc, 9200) or 9200

        # detect scheme (https if xpack.security.enabled=true)
        security = eenv.get("xpack.security.enabled", "false")
        scheme = "https" if security.lower() == "true" else "http"

        # detect auth
        es_user = eenv.get("ELASTIC_USERNAME", "")
        es_pass = eenv.get("ELASTIC_PASSWORD", "")

        if es_user and es_pass:
            local_auth  = f"{es_user}:{es_pass}@"
            docker_auth = f"{es_user}:{es_pass}@"
        else:
            local_auth  = ""
            docker_auth = ""

        local_env["ELASTICSEARCH_URL"]  = f"{scheme}://{local_auth}127.0.0.1:{host_port}"
        local_env["ELASTICSEARCH_HOST"] = "127.0.0.1"
        local_env["ELASTICSEARCH_PORT"] = str(host_port)

        docker_env["ELASTICSEARCH_URL"]  = f"{scheme}://{docker_auth}{elastic_svc}:9200"
        docker_env["ELASTICSEARCH_HOST"] = elastic_svc
        docker_env["ELASTICSEARCH_PORT"] = "9200"

    # ================================================================
    #  FASTAPI — INGESTION SERVICE
    # ================================================================
    if ingestion_svc:
        host_port = get_host_port(services, ingestion_svc, 8000) or 8000

        local_env["INGESTION_SERVICE_URL"]  = f"http://127.0.0.1:{host_port}"
        local_env["INGESTION_SERVICE_PORT"] = str(host_port)

        docker_env["INGESTION_SERVICE_URL"]  = f"http://{ingestion_svc}:8000"
        docker_env["INGESTION_SERVICE_PORT"] = "8000"

    # ================================================================
    #  FASTAPI — GRIDFS SERVICE
    # ================================================================
    if gridfs_svc:
        host_port = get_host_port(services, gridfs_svc, 8001) or 8001

        local_env["GRIDFS_SERVICE_URL"]  = f"http://127.0.0.1:{host_port}"
        local_env["GRIDFS_SERVICE_PORT"] = str(host_port)

        docker_env["GRIDFS_SERVICE_URL"]  = f"http://{gridfs_svc}:8001"
        docker_env["GRIDFS_SERVICE_PORT"] = "8001"

    # ================================================================
    #  STREAMLIT
    # ================================================================
    if streamlit_svc:
        host_port = get_host_port(services, streamlit_svc, 8501) or 8501

        local_env["STREAMLIT_URL"]  = f"http://127.0.0.1:{host_port}"
        local_env["STREAMLIT_PORT"] = str(host_port)

        docker_env["STREAMLIT_URL"]  = f"http://{streamlit_svc}:8501"
        docker_env["STREAMLIT_PORT"] = "8501"

    # ================================================================
    #  WEB UI URLS (browser access — always 127.0.0.1 for both)
    # ================================================================
    if kafka_ui_svc:
        hp = get_host_port(services, kafka_ui_svc, 8080) or 8080
        local_env["KAFKA_UI_URL"]  = f"http://127.0.0.1:{hp}"
        docker_env["KAFKA_UI_URL"] = f"http://127.0.0.1:{hp}"

    if mongo_express_svc:
        hp = get_host_port(services, mongo_express_svc, 8081) or 8081
        local_env["MONGO_EXPRESS_URL"]  = f"http://127.0.0.1:{hp}"
        docker_env["MONGO_EXPRESS_URL"] = f"http://127.0.0.1:{hp}"

    if cloudbeaver_svc:
        hp = get_host_port(services, cloudbeaver_svc, 8978) or 8978
        local_env["CLOUDBEAVER_URL"]  = f"http://127.0.0.1:{hp}"
        docker_env["CLOUDBEAVER_URL"] = f"http://127.0.0.1:{hp}"

    if redisinsight_svc:
        hp = get_host_port(services, redisinsight_svc, 5540) or 5540
        local_env["REDISINSIGHT_URL"]  = f"http://127.0.0.1:{hp}"
        docker_env["REDISINSIGHT_URL"] = f"http://127.0.0.1:{hp}"

    if kibana_svc:
        hp = get_host_port(services, kibana_svc, 5601) or 5601
        local_env["KIBANA_URL"]  = f"http://127.0.0.1:{hp}"
        docker_env["KIBANA_URL"] = f"http://127.0.0.1:{hp}"

    return local_env, docker_env


def main():
    ap = argparse.ArgumentParser(description="Generate .env.local and .env.prod from a docker-compose file")
    ap.add_argument("--compose",      default=COMPOSE_PATH, help="compose yml path")
    ap.add_argument("--out-local",    default=".env.local",  help="output file for local env")
    ap.add_argument("--out-docker",   default=".env.prod",   help="output file for docker env")
    ap.add_argument("--also-dotenv",  choices=["none", "local", "prod"], default="none",
                    help="also write .env from one profile")
    args = ap.parse_args()

    local_env, docker_env = build_envs(args.compose)

    write_env_file(args.out_local, local_env)
    write_env_file(args.out_docker, docker_env)

    print(f"wrote: {args.out_local}  ({len(local_env)} vars)")
    print(f"wrote: {args.out_docker} ({len(docker_env)} vars)")

    if args.also_dotenv == "local":
        write_env_file(".env", local_env)
        print("wrote: .env (from .env.local)")
    elif args.also_dotenv == "prod":
        write_env_file(".env", docker_env)
        print("wrote: .env (from .env.prod)")


if __name__ == "__main__":
    main()
