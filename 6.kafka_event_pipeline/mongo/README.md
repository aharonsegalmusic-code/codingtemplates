# MongoDB Query Patterns Cheatsheet

Reference code for MongoDB query types, wrapped as FastAPI routes. Not a deployable project — use as a lookup when you need MongoDB query syntax.

---

## What's here

- `mongo_db.py` — MongoDB connection setup
- `mongo_insert.py` — Insert one, insert many, bulk write examples
- `mongo_overview.py` — Collection stats and overview queries
- `query_main.py` — All major query types (~14KB): find, filter, sort, limit, skip, projection, aggregation pipeline, `$lookup` (join), `$group`, `$match`, `$unwind`
- `routes_overview.py` — FastAPI routes wrapping overview queries
- `routes_query_main.py` — FastAPI routes wrapping all query types
- `main.py` — App entry point, registers all routes

**Stack:** MongoDB · PyMongo · FastAPI
