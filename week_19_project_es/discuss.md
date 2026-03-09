# Ingestion Service — Code Review & Error Analysis

---

## Overall Assessment

The **logic and structure** of the service is solid. The flow is correct:
`main.py → routes.py → orchestrator → (OCR, metadata, GridFS, Kafka)`.

However, there is **one repeating critical error** that will crash the service at startup — and a few smaller issues.

---

## Critical Error — Repeated in 5 Files

### The Problem: Every module tries to instantiate itself at module-load time, but passes NO arguments to constructors that require them.

Every class in this service has a constructor that **requires** a `logger` (and sometimes more params). Yet at the bottom of each file, an instance is created with **zero arguments**. Python will raise a `TypeError` the moment the module is imported.

| File | Line | Broken Instantiation | What it actually needs |
|---|---|---|---|
| `OCRengine.py` | 46 | `ocr_engine = OCREngine()` | `OCREngine(logger)` |
| `metadata_extractor.py` | 57 | `metadata = MetadataExtractor()` | `MetadataExtractor(logger)` |
| `kafka_publisher.py` | 48 | `publisher = KafkaPublisher()` | `KafkaPublisher(bootstrap_servers, topic_name, logger)` |
| `mongo_client.py` | 51 | `Gridfs = MongoLoaderClient()` | `MongoLoaderClient(gridfs_service_url, logger)` |
| `ingestion_orchestrator.py` | 109 | `orchestrator = IngestionOrchestrator()` | `IngestionOrchestrator(config, ocr_engine, metadata, Gridfs, publisher, logger)` |

**The crash chain:** When Python runs `main.py`, it imports `routes.py`, which imports `ingestion_orchestrator.py`, which imports all the other modules — each one blows up on its last line before any real code even runs.

The error you will see looks like:
```
TypeError: OCREngine.__init__() missing 1 required positional argument: 'logger'
```

---

## Root Cause — Design Mismatch

The **intended design** (documented in every docstring) is **dependency injection**:
- `main.py` creates the logger
- `main.py` builds each component, passing the logger in
- Components are wired together and passed to the orchestrator

**What actually happened:** Every module independently tried to create its own singleton at the bottom, but the logger (and other dependencies) doesn't exist yet at that point.

The fix is simple: `main.py` needs to actually instantiate and wire all the components together — the plumbing that was planned but never written.

---

## Secondary Issues

### 1. `mongo_client.py` — Wrong import path + unused import (line 8)

```python
from ingestion_service_api.ingestion_config import IngestionConfig
```

- All other files use local imports: `from ingestion_config import ...`
- This uses an absolute package path that will fail depending on how the service is run
- **Worse: `IngestionConfig` is imported but never used in this file** — it's dead code

---

### 2. `routes.py` — Confusing self-shadowing variable (lines 7–13)

```python
from ingestion_orchestrator import IngestionOrchestrator
from ingestion_orchestrator import orchestrator

router = APIRouter()
orchestrator: IngestionOrchestrator = orchestrator   # <-- reassigns itself
```

The line `orchestrator: IngestionOrchestrator = orchestrator` is just a type annotation on an import — it does nothing functional. The intent was probably to receive the orchestrator from `main.py` via injection, but that wiring was never built. This is a leftover placeholder.

---

### 3. `main.py` — Logger created but never passed anywhere

```python
logger = get_logger("ingestion-service")
app = FastAPI(title="Ingestion Service")
app.include_router(router)
```

`main.py` creates a logger but never uses it to build any of the service components. The entire wiring step — creating `OCREngine(logger)`, `MetadataExtractor(logger)`, etc. — is missing. The logger just sits there unused.

---

## Summary

| # | Severity | Issue | Location |
|---|---|---|---|
| 1 | CRITICAL | `OCREngine()` called with no args | `OCRengine.py:46` |
| 2 | CRITICAL | `MetadataExtractor()` called with no args | `metadata_extractor.py:57` |
| 3 | CRITICAL | `KafkaPublisher()` called with no args | `kafka_publisher.py:48` |
| 4 | CRITICAL | `MongoLoaderClient()` called with no args | `mongo_client.py:51` |
| 5 | CRITICAL | `IngestionOrchestrator()` called with no args | `ingestion_orchestrator.py:109` |
| 6 | MEDIUM | Wrong import path + unused import | `mongo_client.py:8` |
| 7 | LOW | Logger created but never wired to components | `main.py` |
| 8 | LOW | Redundant self-shadowing orchestrator variable | `routes.py:13` |

---

## What Needs to Happen

`main.py` needs to be the **composition root** — the single place that:
1. Creates the logger
2. Creates the config
3. Creates each component (OCREngine, MetadataExtractor, MongoLoaderClient, KafkaPublisher) — passing the logger and config values in
4. Creates the orchestrator — passing all components in
5. Passes the orchestrator to the router

The classes themselves are written correctly. The wiring between them is what's missing.
